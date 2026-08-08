import "./styles.css";
import { BOND } from "./engine";

type WorkerReply = { id: number; ok: boolean; result?: unknown; error?: string };
type CalculateResult = { responses: number[][]; elapsedMs: number; arfSum: number; genus: number; sectors: string };
type ExactRow = { prime: string; n: number; sharedMs: number; literalMs: number; agrees: boolean; checksum: string };
type BenchmarkResult = {
  generatedAt: string;
  weights: { tx: number; ty: number; tz: number };
  sharedRows: { n: number; ms: number; measured: boolean }[];
  comparisonRows: { n: number; sharedMs: number; separateMs: number; speedup: number }[];
  literalRows: { n: number; ms: number; sectors: number; measured: boolean }[];
  coreApplication: {
    structuredMs: number;
    denseMs: number;
    denseConstructionMs: number;
    maxDifference: number;
    oneDenseCoreBytes: number;
    allDenseCoresAtN100Bytes: number;
    structuredStateBytes: number;
  };
  note: string;
};

const app = document.querySelector<HTMLDivElement>("#app");
if (!app) throw new Error("missing app root");

app.innerHTML = `
  <header class="hero">
    <div class="hero-copy">
      <p class="eyebrow">Exact width-three spin-structure engine</p>
      <h1>Where Did the <span>4<sup>g</sup></span> Ising Sectors Go?</h1>
      <p class="lede">The complete pre-Arf family is propagated through a fixed 256-state even-mask carrier. Change the strip, inspect every handle response, and benchmark the contraction paths yourself.</p>
      <div class="claim"><b>Scope:</b> fixed-width cubic-lattice strips. This does not make the three-dimensional Ising model efficient when width grows.</div>
    </div>
    <div class="formula-card"><code>G<sub>n,3</sub> = P<sub>n</sub> □ P<sub>3</sub> □ P<sub>3</sub></code><strong>d = 2<sup>9−1</sup> = 256</strong><small>independent of strip length n</small></div>
  </header>

  <main>
    <section class="control-strip panel">
      <label>Length <output id="n-output">20</output><input id="n" type="range" min="2" max="100" value="20"></label>
      <label>Selected handle <output id="handle-output">1</output><input id="handle" type="range" min="1" max="19" value="1"></label>
      <label>t<sub>x</sub> <output id="tx-output">0.220</output><input id="tx" type="range" min="0.02" max="0.30" step="0.005" value="0.22"></label>
      <label>t<sub>y</sub> <output id="ty-output">0.220</output><input id="ty" type="range" min="0.02" max="0.30" step="0.005" value="0.22"></label>
      <label>t<sub>z</sub> <output id="tz-output">0.220</output><input id="tz" type="range" min="0.02" max="0.30" step="0.005" value="0.22"></label>
      <label class="toggle"><input id="isotropic" type="checkbox" checked><span></span> isotropic</label>
      <label>Selected-slab perturbation <output id="perturb-output">1.00×</output><input id="perturb" type="range" min="0.50" max="1.50" step="0.05" value="1"></label>
    </section>

    <section class="top-grid">
      <article class="panel lattice-panel">
        <div class="section-head"><div><p class="eyebrow">Geometry</p><h2>A moving nine-bit separator</h2></div><span id="separator-label" class="badge">handle 1</span></div>
        <svg id="lattice" viewBox="0 0 760 360" role="img" aria-label="Three by three cubic-lattice strip"></svg>
        <div class="legend"><span><i class="dot lattice-dot"></i> grid vertex</span><span><i class="dot separator-dot"></i> frontier mask site</span><span><i class="line handle-line"></i> selected co-core</span></div>
      </article>

      <article class="panel complexity-panel">
        <div class="section-head"><div><p class="eyebrow">Complexity</p><h2>The sector count moves. The bond does not.</h2></div></div>
        <dl class="metrics">
          <div><dt>Length n</dt><dd id="metric-n">20</dd></div>
          <div><dt>Genus g</dt><dd id="metric-g">19</dd></div>
          <div class="accent"><dt>Literal sectors</dt><dd id="metric-sectors">274,877,906,944</dd></div>
          <div><dt>Compressed bond</dt><dd>256</dd></div>
          <div><dt>Literal values × 8 bytes</dt><dd id="metric-literal-memory"></dd></div>
          <div><dt>Two environment sweeps</dt><dd id="metric-compressed-memory"></dd></div>
        </dl>
        <div class="growth-track"><div id="growth-fill"></div></div>
        <p class="micro">The explicit-sector estimate counts one scalar per sector only; a real per-sector Pfaffian workflow costs more.</p>
      </article>
    </section>

    <section class="panel response-panel">
      <div class="section-head"><div><p class="eyebrow">All-sector response</p><h2>Four Walsh characters at every handle</h2></div><div class="status" id="response-status">calculating…</div></div>
      <div class="heatmap-wrap"><div class="heatmap-labels"><span>00</span><span>10</span><span>01</span><span>11</span></div><div id="heatmap" class="heatmap"></div></div>
      <div class="response-footer"><span>teal: negative</span><span>cream: near zero</span><span>coral: positive</span><span id="arf-value"></span></div>
    </section>

    <section class="benchmark-grid">
      <article class="panel benchmark-panel">
        <div class="section-head"><div><p class="eyebrow">Measured locally</p><h2>Contraction benchmark</h2></div><button id="run-benchmark">Run benchmark</button></div>
        <div id="benchmark-empty" class="empty-state">Run the benchmark to compare literal enumeration, separate contractions, shared environments, and one dense-versus-structured core.</div>
        <div id="benchmark-results" hidden></div>
      </article>
      <article class="panel exact-panel">
        <div class="section-head"><div><p class="eyebrow">Exact audit</p><h2>Two-prime reference mode</h2></div><button id="run-exact">Check current n</button></div>
        <p>Uses weights (t<sub>x</sub>,t<sub>y</sub>,t<sub>z</sub>)=(2,3,5) in each finite field and compares the shared sweep with literal sector enumeration. Capped at n=7 by design.</p>
        <div id="exact-results" class="exact-results"><span class="muted">Not run yet.</span></div>
      </article>
    </section>

    <section class="panel architecture">
      <p class="eyebrow">What the browser actually applies</p>
      <div class="pipeline"><div><b>Parity flips</b><span>12 sparse XOR transitions</span></div><em>→</em><div><b>Connector</b><span>mask diagonal</span></div><em>→</em><div><b>Gauge phase</b><span>two sign diagonals</span></div><em>→</em><div><b>Local Gauss</b><span>4×4 Walsh kernel</span></div></div>
      <p class="micro">No collection of generic 256×256 matrices is stored. The dense benchmark materializes one representative core only. WebGPU is intentionally not implemented in this first build.</p>
    </section>
  </main>

  <footer><span>Hainan Zhao · Lane B structural Ising project</span><button id="export" disabled>Export benchmark JSON</button></footer>
`;

const worker = new Worker(new URL("./worker.ts", import.meta.url), { type: "module" });
let nextRequest = 1;
const pending = new Map<number, { resolve: (value: unknown) => void; reject: (error: Error) => void }>();
worker.onmessage = (event: MessageEvent<WorkerReply>) => {
  const entry = pending.get(event.data.id);
  if (!entry) return;
  pending.delete(event.data.id);
  if (event.data.ok) entry.resolve(event.data.result);
  else entry.reject(new Error(event.data.error ?? "worker error"));
};

function request<T>(payload: Omit<Record<string, unknown>, "id">): Promise<T> {
  const id = nextRequest++;
  return new Promise((resolve, reject) => {
    pending.set(id, { resolve: resolve as (value: unknown) => void, reject });
    worker.postMessage({ id, ...payload });
  });
}

function byId<T extends Element = HTMLElement>(id: string): T {
  const element = document.getElementById(id);
  if (!element) throw new Error(`missing #${id}`);
  return element as unknown as T;
}

const controls = {
  n: byId<HTMLInputElement>("n"), handle: byId<HTMLInputElement>("handle"),
  tx: byId<HTMLInputElement>("tx"), ty: byId<HTMLInputElement>("ty"), tz: byId<HTMLInputElement>("tz"),
  isotropic: byId<HTMLInputElement>("isotropic"), perturb: byId<HTMLInputElement>("perturb"),
};
let latestCalculation = 0;
let lastBenchmark: BenchmarkResult | null = null;

function formatInteger(value: bigint): string { return value.toLocaleString("en-US"); }
function formatBytes(value: number | bigint): string {
  const numeric = typeof value === "bigint" ? Number(value) : value;
  if (!Number.isFinite(numeric)) return ">10³⁰⁰ bytes";
  const units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"];
  let scaled = numeric; let unit = 0;
  while (scaled >= 1024 && unit < units.length - 1) { scaled /= 1024; unit += 1; }
  return `${scaled >= 100 ? scaled.toFixed(0) : scaled.toFixed(1)} ${units[unit]}`;
}
function formatFloat(value: number): string {
  if (!Number.isFinite(value)) return "overflow";
  const magnitude = Math.abs(value);
  return magnitude === 0 ? "0" : magnitude > 1e6 || magnitude < 1e-3 ? value.toExponential(3) : value.toPrecision(5);
}

function state() {
  return {
    n: Number(controls.n.value), handle: Number(controls.handle.value) - 1,
    tx: Number(controls.tx.value), ty: Number(controls.ty.value), tz: Number(controls.tz.value),
    perturbFactor: Number(controls.perturb.value),
  };
}

function updateCounters(): void {
  const { n, handle, tx, ty, tz, perturbFactor } = state();
  const genus = n - 1;
  controls.handle.max = String(genus);
  if (handle >= genus) controls.handle.value = String(genus);
  byId("n-output").textContent = String(n);
  byId("handle-output").textContent = controls.handle.value;
  byId("tx-output").textContent = tx.toFixed(3);
  byId("ty-output").textContent = ty.toFixed(3);
  byId("tz-output").textContent = tz.toFixed(3);
  byId("perturb-output").textContent = `${perturbFactor.toFixed(2)}×`;
  byId("metric-n").textContent = String(n);
  byId("metric-g").textContent = String(genus);
  const sectors = 1n << BigInt(2 * genus);
  byId("metric-sectors").textContent = formatInteger(sectors);
  byId("metric-literal-memory").textContent = formatBytes(sectors * 8n);
  byId("metric-compressed-memory").textContent = formatBytes(2 * (genus + 1) * BOND * 8);
  byId("separator-label").textContent = `handle ${Number(controls.handle.value)}`;
  byId<HTMLDivElement>("growth-fill").style.width = `${Math.min(100, 8 + genus * 0.92)}%`;
}

function renderLattice(): void {
  const svg = byId<SVGSVGElement>("lattice");
  const { n } = state();
  const selected = Number(controls.handle.value) - 1;
  const shown = Math.min(n, 13);
  const xScale = 610 / Math.max(1, shown - 1);
  const point = (slice: number, y: number, z: number) => ({
    x: 70 + slice * xScale + y * 15,
    y: 275 - z * 52 - y * 18,
  });
  const lines: string[] = [];
  for (let s = 0; s < shown; s += 1) {
    for (let y = 0; y < 3; y += 1) for (let z = 0; z < 3; z += 1) {
      const p = point(s, y, z);
      if (z < 2) { const q = point(s, y, z + 1); lines.push(`<line x1="${p.x}" y1="${p.y}" x2="${q.x}" y2="${q.y}"/>`); }
      if (y < 2) { const q = point(s, y + 1, z); lines.push(`<line x1="${p.x}" y1="${p.y}" x2="${q.x}" y2="${q.y}"/>`); }
      if (s < shown - 1) { const q = point(s + 1, y, z); lines.push(`<line x1="${p.x}" y1="${p.y}" x2="${q.x}" y2="${q.y}"/>`); }
    }
  }
  const visualHandle = n <= shown ? selected : Math.round(selected * (shown - 2) / Math.max(1, n - 2));
  const separatorX = (point(Math.min(shown - 2, visualHandle), 0, 0).x + point(Math.min(shown - 1, visualHandle + 1), 0, 0).x) / 2;
  const dots: string[] = [];
  for (let y = 0; y < 3; y += 1) for (let z = 0; z < 3; z += 1) {
    const p = point(Math.min(shown - 1, visualHandle + 1), y, z);
    dots.push(`<circle class="separator-site" cx="${separatorX + y * 15}" cy="${p.y}" r="6"/>`);
  }
  const square = [point(Math.min(shown - 1, visualHandle + 1), 1, 0), point(Math.min(shown - 1, visualHandle + 1), 2, 0), point(Math.min(shown - 1, visualHandle + 1), 2, 1), point(Math.min(shown - 1, visualHandle + 1), 1, 1)];
  svg.innerHTML = `<g class="grid-lines">${lines.join("")}</g><line class="separator-plane" x1="${separatorX - 12}" y1="66" x2="${separatorX + 35}" y2="300"/>${dots.join("")}<polygon class="handle-square" points="${square.map((p) => `${p.x},${p.y}`).join(" ")}"/><text x="34" y="330">slice 1</text><text x="680" y="330">slice ${n}</text>${n > shown ? `<text class="ellipsis" x="675" y="285">⋯</text>` : ""}`;
}

function renderHeatmap(responses: number[][]): void {
  const heatmap = byId("heatmap");
  const selected = Number(controls.handle.value) - 1;
  heatmap.style.setProperty("--rows", String(responses.length));
  heatmap.innerHTML = responses.map((row, i) => {
    const max = Math.max(...row.map((value) => Math.abs(value)), 1e-300);
    return `<div class="heat-row ${i === selected ? "selected" : ""}" data-handle="${i + 1}"><b>${i + 1}</b>${row.map((value, character) => {
      const strength = Math.min(1, Math.sqrt(Math.abs(value) / max));
      const color = value >= 0 ? `rgba(238,112,82,${0.12 + 0.82 * strength})` : `rgba(34,139,143,${0.12 + 0.82 * strength})`;
      return `<button title="M_${i + 1}(${["00", "10", "01", "11"][character]}) = ${formatFloat(value)}" style="background:${color}">${formatFloat(value / max)}</button>`;
    }).join("")}</div>`;
  }).join("");
  heatmap.querySelectorAll<HTMLElement>(".heat-row").forEach((row) => row.addEventListener("click", () => {
    controls.handle.value = row.dataset.handle ?? "1"; refresh();
  }));
}

async function calculate(): Promise<void> {
  const serial = ++latestCalculation;
  const current = state();
  byId("response-status").textContent = "calculating structured sweep…";
  try {
    const result = await request<CalculateResult>({ type: "calculate", ...current, perturbHandle: current.handle });
    if (serial !== latestCalculation) return;
    renderHeatmap(result.responses);
    byId("response-status").textContent = `${result.responses.length * 4} responses · ${result.elapsedMs.toFixed(1)} ms`;
    byId("arf-value").textContent = `Arf-weighted sum: ${formatFloat(result.arfSum)}`;
  } catch (error) {
    byId("response-status").textContent = error instanceof Error ? error.message : String(error);
  }
}

let debounce = 0;
function refresh(): void {
  updateCounters(); renderLattice();
  window.clearTimeout(debounce);
  debounce = window.setTimeout(() => void calculate(), 80);
}

function renderBenchmark(result: BenchmarkResult): void {
  const maxMs = Math.max(...result.sharedRows.map((row) => row.ms), ...result.literalRows.map((row) => row.ms), 1);
  const points = result.sharedRows.map((row, i) => `${25 + i * 75},${175 - 140 * Math.log1p(row.ms) / Math.log1p(maxMs)}`).join(" ");
  byId("benchmark-empty").hidden = true;
  const container = byId("benchmark-results");
  container.hidden = false;
  container.innerHTML = `
    <svg class="runtime-chart" viewBox="0 0 510 205" aria-label="Measured shared-environment runtime versus strip length"><line x1="25" y1="175" x2="490" y2="175"/><line x1="25" y1="20" x2="25" y2="175"/><polyline points="${points}"/>${result.sharedRows.map((row, i) => `<circle cx="${25 + i * 75}" cy="${175 - 140 * Math.log1p(row.ms) / Math.log1p(maxMs)}" r="4"/><text x="${20 + i * 75}" y="195">${row.n}</text>`).join("")}<text x="175" y="15">shared sweep: measured, approximately linear</text></svg>
    <div class="benchmark-cards">
      <div><span>Shared vs separate at n=10</span><b>${result.comparisonRows.at(-1)?.speedup.toFixed(2)}×</b></div>
      <div><span>Structured core apply</span><b>${result.coreApplication.structuredMs.toFixed(2)} ms</b></div>
      <div><span>Dense core apply</span><b>${result.coreApplication.denseMs.toFixed(2)} ms</b></div>
      <div><span>Dense construction</span><b>${result.coreApplication.denseConstructionMs.toFixed(1)} ms</b></div>
    </div>
    <table><thead><tr><th>n</th><th>shared</th><th>separate</th><th>speedup</th></tr></thead><tbody>${result.comparisonRows.map((row) => `<tr><td>${row.n}</td><td>${row.sharedMs.toFixed(1)} ms</td><td>${row.separateMs.toFixed(1)} ms</td><td>${row.speedup.toFixed(2)}×</td></tr>`).join("")}</tbody></table>
    <p class="micro">Literal measurements stop at n=5 (${result.literalRows.at(-1)?.sectors} sectors). No unmeasured point is presented as a runtime. One dense core uses ${formatBytes(result.coreApplication.oneDenseCoreBytes)}; storing four dense cores for every handle at n=100 would use ${formatBytes(result.coreApplication.allDenseCoresAtN100Bytes)}.</p>`;
}

byId<HTMLButtonElement>("run-benchmark").addEventListener("click", async (event) => {
  const button = event.currentTarget as HTMLButtonElement; button.disabled = true; button.textContent = "Running…";
  try {
    const { tx, ty, tz } = state();
    lastBenchmark = await request<BenchmarkResult>({ type: "benchmark", tx, ty, tz });
    renderBenchmark(lastBenchmark);
    byId<HTMLButtonElement>("export").disabled = false;
  } finally { button.disabled = false; button.textContent = "Run benchmark"; }
});

byId<HTMLButtonElement>("run-exact").addEventListener("click", async (event) => {
  const button = event.currentTarget as HTMLButtonElement; button.disabled = true; button.textContent = "Checking…";
  const target = byId("exact-results"); target.innerHTML = `<span class="muted">Exact BigInt replay is running in a worker…</span>`;
  try {
    const rows = await request<ExactRow[]>({ type: "exact", n: Math.min(7, state().n) });
    target.innerHTML = rows.map((row) => `<div class="exact-row ${row.agrees ? "pass" : "fail"}"><b>GF(${row.prime})</b><span>${row.agrees ? "exact agreement" : "mismatch"}</span><small>shared ${row.sharedMs.toFixed(1)} ms · literal ${row.literalMs.toFixed(1)} ms · ${row.checksum}</small></div>`).join("");
  } catch (error) { target.textContent = error instanceof Error ? error.message : String(error); }
  finally { button.disabled = false; button.textContent = "Check current n"; }
});

byId<HTMLButtonElement>("export").addEventListener("click", () => {
  if (!lastBenchmark) return;
  const blob = new Blob([JSON.stringify(lastBenchmark, null, 2)], { type: "application/json" });
  const link = document.createElement("a"); link.href = URL.createObjectURL(blob); link.download = "ising-twist-response-benchmark.json"; link.click(); URL.revokeObjectURL(link.href);
});

controls.isotropic.addEventListener("change", () => {
  controls.ty.disabled = controls.isotropic.checked; controls.tz.disabled = controls.isotropic.checked;
  if (controls.isotropic.checked) { controls.ty.value = controls.tx.value; controls.tz.value = controls.tx.value; }
  refresh();
});
controls.tx.addEventListener("input", () => {
  if (controls.isotropic.checked) { controls.ty.value = controls.tx.value; controls.tz.value = controls.tx.value; }
  refresh();
});
[controls.n, controls.handle, controls.ty, controls.tz, controls.perturb].forEach((control) => control.addEventListener("input", refresh));

controls.ty.disabled = true; controls.tz.disabled = true;
refresh();
