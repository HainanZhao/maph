import "./styles.css";
import { exactRoute, output, type Pool } from "./model";

const BASE: Pool[] = [
  { name: "Pool A", inputReserve: 1000, outputReserve: 1220, fee: 0.997, fixedCost: 1.5 },
  { name: "Pool B", inputReserve: 1850, outputReserve: 2210, fee: 0.997, fixedCost: 3.2 },
  { name: "Pool C", inputReserve: 700, outputReserve: 875, fee: 0.996, fixedCost: 5.1 },
  { name: "Pool D", inputReserve: 3100, outputReserve: 3720, fee: 0.999, fixedCost: 7.4 },
];
const app = document.querySelector<HTMLDivElement>("#app");
if (!app) throw new Error("missing app");
app.innerHTML = `<header><a href="../../">← Research demos</a><p class="eyebrow">A small exact routing laboratory</p><h1>When is another route<br><em>worth its gas?</em></h1><p>A swap can be split across pools. Better prices favour splitting; a fixed execution cost favours using fewer pools. This page checks every active set of four displayed pools and optimizes each selected set.</p></header><main><section class="warning"><b>Not financial advice.</b> These are synthetic pools. The result is an illustrative calculation for a narrow parallel constant-product model, not a live quote or a recommendation to trade.</section><section class="controls panel"><label>Input amount <output id="amount-value"></output><input id="amount" type="range" min="20" max="1000" step="10" value="300"></label><label>Gas multiplier <output id="gas-value"></output><input id="gas" type="range" min="0" max="4" step="0.1" value="1"></label></section><section class="grid"><article class="panel"><p class="eyebrow">Exact active-set result</p><h2 id="headline"></h2><div id="allocations" class="allocations"></div><div class="totals"><div><span>Gross output</span><b id="gross"></b></div><div><span>Fixed gas</span><b id="fixed"></b></div><div><span>Net output</span><b id="net"></b></div></div></article><article class="panel compare"><p class="eyebrow">Why selection matters</p><h2 id="single-headline"></h2><p id="comparison"></p><div id="mini-bars" class="mini-bars"></div></article></section><section class="panel method"><div><p class="eyebrow">What the project contributes</p><h2>Separate price improvement from fixed-cost selection.</h2></div><p>For a chosen set of pools, the continuous allocation is a water-filling problem. The hard part is deciding which pools deserve activation. This small page enumerates all 15 nonempty active sets, so it is an exact control for four pools; the project investigates faster exact and certifiable methods for larger structured instances.</p></section><footer><b>OBSERVED calculation:</b> browser values use floating-point arithmetic. Changing gas should visibly change which pools activate.</footer></main>`;
const amount = document.querySelector<HTMLInputElement>("#amount")!;
const gas = document.querySelector<HTMLInputElement>("#gas")!;
const f = (value: number) => value.toFixed(3);
function render(): void {
  const Q = Number(amount.value); const multiplier = Number(gas.value);
  const pools = BASE.map((pool) => ({ ...pool, fixedCost: pool.fixedCost * multiplier }));
  const best = exactRoute(pools, Q);
  const singles = pools.map((pool) => output(pool, Q) - pool.fixedCost);
  const bestSingle = Math.max(...singles);
  document.querySelector("#amount-value")!.textContent = `${Q} X`;
  document.querySelector("#gas-value")!.textContent = `${multiplier.toFixed(1)}×`;
  document.querySelector("#headline")!.textContent = `${best.active.length} of 4 pools are worth activating`;
  document.querySelector("#allocations")!.innerHTML = pools.map((pool, index) => `<div class="allocation ${best.active.includes(index) ? "on" : ""}"><b>${pool.name}</b><span>${f(best.allocation[index] ?? 0)} X</span><i style="width:${Math.min(100, 100 * (best.allocation[index] ?? 0) / Q)}%"></i></div>`).join("");
  document.querySelector("#gross")!.textContent = f(best.gross);
  document.querySelector("#fixed")!.textContent = `−${f(best.fixed)}`;
  document.querySelector("#net")!.textContent = f(best.net);
  document.querySelector("#single-headline")!.textContent = `Best one-pool route: ${f(bestSingle)}`;
  document.querySelector("#comparison")!.textContent = best.net >= bestSingle ? `Splitting gains ${f(best.net - bestSingle)} net output after fixed costs.` : "The best route uses only one pool at this setting.";
  const values = [...singles, best.net]; const scale = Math.max(...values.map(Math.abs), 1);
  document.querySelector("#mini-bars")!.innerHTML = [...singles.map((value, index) => ({ label: BASE[index]!.name, value })), { label: "exact best", value: best.net }].map(({ label, value }) => `<div><span>${label}</span><i style="width:${Math.max(1, 100 * value / scale)}%"></i><b>${f(value)}</b></div>`).join("");
}
[amount, gas].forEach((input) => input.addEventListener("input", render));render();
