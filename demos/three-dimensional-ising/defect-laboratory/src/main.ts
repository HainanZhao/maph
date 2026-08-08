import "./styles.css";
import { BOND } from "../../twist-response/src/engine";

type Result = { baseline: number[][]; perturbed: number[][]; delta: number[][]; scale: number; elapsedMs: number };
type Reply = { id: number; ok: boolean; result?: Result; error?: string };

const app = document.querySelector<HTMLDivElement>("#app");
if (!app) throw new Error("missing app");

app.innerHTML = `
  <header class="hero">
    <a href="../../">← Research demos</a>
    <p class="eyebrow">The theorem doing useful work</p>
    <h1>Touch one defect.<br><em>See every response.</em></h1>
    <p>Strengthen or weaken one slab in a long, thin Ising strip. The calculator preserves the entire spin-structure family and reports how every handle response changes.</p>
  </header>
  <main>
    <section class="claim"><b>Actual scope:</b> an exact structured engine for fixed-width <code>3×3×n</code> strips. It compares an unperturbed strip with one local coupling perturbation. It is not a material-design prediction or a solution of growing three-dimensional cubes.</section>
    <section class="panel controls">
      <label>Strip length <output id="n-value">30</output><input id="n" type="range" min="2" max="100" value="30"></label>
      <label>Defect location <output id="defect-value">15</output><input id="defect" type="range" min="1" max="29" value="15"></label>
      <label>Local coupling <output id="factor-value">0.70×</output><input id="factor" type="range" min="0.50" max="1.50" step="0.05" value="0.70"></label>
      <label>Base coupling <output id="coupling-value">0.220</output><input id="coupling" type="range" min="0.04" max="0.30" step="0.005" value="0.22"></label>
    </section>
    <section class="grid">
      <article class="panel strip">
        <div class="section-head"><div><p class="eyebrow">The intervention</p><h2>A single changed slab</h2></div><span id="run-state">calculating…</span></div>
        <div id="strip-diagram" class="strip-diagram" role="img" aria-label="A long strip with one highlighted defect"></div>
        <p>Orange is the local defect. Each position below is one handle whose four sector responses are evaluated together.</p>
      </article>
      <article class="panel difference">
        <p class="eyebrow">What compression buys</p><h2 id="sector-count"></h2><p>possible sector choices would be retained separately by literal enumeration.</p>
        <div class="equals">↓</div><strong>256 states</strong><p>are carried by the structured separator engine, regardless of strip length.</p>
        <dl><div><dt>Calculated now</dt><dd id="elapsed">—</dd></div><div><dt>Returned now</dt><dd id="returned">—</dd></div><div><dt>Carrier</dt><dd>${BOND} states</dd></div></dl>
      </article>
    </section>
    <section class="panel map-panel">
      <div class="section-head"><div><p class="eyebrow">All-handle defect map</p><h2>Relative response to one local change</h2></div><span>Click any row to inspect it</span></div>
      <p class="legend"><i class="negative"></i> response decreases <i class="zero"></i> little change <i class="positive"></i> response increases. Colours are normalized to the largest change in this current run.</p>
      <div class="labels"><span>handle</span><span>00</span><span>10</span><span>01</span><span>11</span></div><div id="response-map" class="response-map"></div>
      <div id="detail" class="detail">Select a handle response to compare its before-and-after values.</div>
    </section>
    <section class="panel why">
      <div><p class="eyebrow">Why this is different from a toy animation</p><h2>The map above is calculated from the full sector family.</h2></div>
      <p>For this fixed-width strip, the theorem gives a shared 256-state carrier. That is why the tool can return all <code>4g</code> single-handle Walsh responses after changing one defect, rather than displaying one chosen sector or sampling a few cases. For small strips, the companion engine can also compare against literal sector enumeration.</p>
      <a href="../twist-response/">Open the exact engine and its brute-force controls →</a>
    </section>
    <footer><b>OBSERVED browser output</b> — floating-point values depend on the selected couplings. The structural compression is limited to the displayed fixed width.</footer>
  </main>
`;

const byId = <T extends Element = HTMLElement>(id: string) => {
  const element = document.getElementById(id);
  if (!element) throw new Error(`missing ${id}`);
  return element as unknown as T;
};
const nInput = byId<HTMLInputElement>("n");
const defectInput = byId<HTMLInputElement>("defect");
const factorInput = byId<HTMLInputElement>("factor");
const couplingInput = byId<HTMLInputElement>("coupling");
const worker = new Worker(new URL("./worker.ts", import.meta.url), { type: "module" });
let requestId = 0;
let latest: Result | null = null;
let selected = -1;

function state() {
  const n = Number(nInput.value);
  return { n, defect: Math.min(n - 2, Number(defectInput.value) - 1), factor: Number(factorInput.value), coupling: Number(couplingInput.value) };
}
function number(value: number): string { return Number.isFinite(value) ? (Math.abs(value) < 1e-4 && value !== 0 ? value.toExponential(2) : value.toPrecision(5)) : "overflow"; }
function updateControls(): void {
  const { n, defect, factor, coupling } = state();
  defectInput.max = String(n - 1);
  if (Number(defectInput.value) > n - 1) defectInput.value = String(n - 1);
  byId("n-value").textContent = String(n);
  byId("defect-value").textContent = String(defect + 1);
  byId("factor-value").textContent = `${factor.toFixed(2)}×`;
  byId("coupling-value").textContent = coupling.toFixed(3);
  byId("sector-count").textContent = `4^${n - 1} = ${(1n << BigInt(2 * (n - 1))).toLocaleString("en-US")}`;
  const shown = Math.min(n - 1, 40);
  const defectVisual = Math.round(defect * (shown - 1) / Math.max(1, n - 2));
  byId("strip-diagram").innerHTML = Array.from({ length: shown }, (_, i) => `<button class="${i === defectVisual ? "defect" : ""}" aria-label="${i === defectVisual ? "changed local coupling" : "ordinary slab"}"></button>`).join("") + (n - 1 > shown ? "<b>…</b>" : "");
}
function showDetail(index: number): void {
  if (!latest) return;
  selected = index;
  const before = latest.baseline[index] ?? [];
  const after = latest.perturbed[index] ?? [];
  const delta = latest.delta[index] ?? [];
  byId("detail").innerHTML = `<b>Handle ${index + 1}</b><span>before → after</span>${["00", "10", "01", "11"].map((label, i) => `<code>${label}: ${number(before[i] ?? 0)} → ${number(after[i] ?? 0)} &nbsp; Δ ${number(delta[i] ?? 0)}</code>`).join("")}`;
  renderMap();
}
function renderMap(): void {
  if (!latest) return;
  const map = byId("response-map");
  map.innerHTML = latest.delta.map((row, handle) => `<button class="map-row ${handle === selected ? "selected" : ""}" data-handle="${handle}"><b>${handle + 1}</b>${row.map((value) => {
    const intensity = Math.min(1, Math.sqrt(Math.abs(value) / latest!.scale));
    const hue = value >= 0 ? `rgba(224,101,74,${0.12 + intensity * 0.82})` : `rgba(42,117,143,${0.12 + intensity * 0.82})`;
    return `<span style="background:${hue}">${number(value / latest!.scale)}</span>`;
  }).join("")}</button>`).join("");
  map.querySelectorAll<HTMLButtonElement>("[data-handle]").forEach((row) => row.addEventListener("click", () => showDetail(Number(row.dataset.handle))));
}
function calculate(): void {
  updateControls();
  byId("run-state").textContent = "calculating…";
  const id = ++requestId;
  const { n, defect, factor, coupling } = state();
  worker.postMessage({ id, n, defect, factor, tx: coupling, ty: coupling, tz: coupling });
}
worker.onmessage = (event: MessageEvent<Reply>) => {
  if (event.data.id !== requestId) return;
  if (!event.data.ok || !event.data.result) { byId("run-state").textContent = event.data.error ?? "calculation failed"; return; }
  latest = event.data.result;
  byId("run-state").textContent = "compressed calculation complete";
  byId("elapsed").textContent = `${latest.elapsedMs.toFixed(1)} ms`;
  byId("returned").textContent = `${latest.delta.length * 4} response values`;
  showDetail(Math.min(state().defect, latest.delta.length - 1));
};
[nInput, defectInput, factorInput, couplingInput].forEach((input) => input.addEventListener("input", calculate));
calculate();
