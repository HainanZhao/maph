import "./styles.css";
import { fibonacci, isSymmetric, isUnimodal, widthFourCoefficients } from "./model";

const app = document.querySelector<HTMLDivElement>("#app");
if (!app) throw new Error("missing app");
app.innerHTML = `<header><a href="../../">← Research demos</a><p class="eyebrow">A proved infinite family</p><h1>The q-Fibonomial<br><em>mountain</em></h1><p>Move through a family of polynomials. Every bar is an exact integer coefficient; the theorem says the bars never go back up after they start going down.</p></header><main><section class="panel controls"><label>Choose m <output id="m-value">5</output><input id="m" type="range" min="1" max="10" value="5"></label><div><span>Polynomial</span><strong id="formula"></strong></div><div><span>Fibonacci inputs</span><strong id="fib"></strong></div></section><section class="panel chart-panel"><div class="head"><div><p class="eyebrow">Exact coefficients</p><h2 id="degree"></h2></div><span id="verdict">checking…</span></div><div id="chart" class="chart" aria-label="q-Fibonomial coefficient chart"></div><div class="axis"><span>q⁰</span><span>middle</span><span>qᴰ</span></div></section><section class="explain"><article><p class="eyebrow">The result</p><h2>For every m ≥ 1, this mountain is unimodal.</h2><p>The displayed polynomial is the width-four q-Fibonomial coefficient \([\!\binom{m+4}{4}\!]_{\mathcal F}\). The theorem covers the full infinite family, not just the ten examples on this page.</p></article><article><p class="eyebrow">What “unimodal” means</p><h2>Rise, perhaps flatten, then fall.</h2><p>The chart is also symmetric: its right half mirrors the left. The page computes coefficients exactly with integer arithmetic; the theorem is stronger than this finite visual check.</p></article></section><footer><b>PROVED theorem:</b> width-four q-Fibonomial coefficients are unimodal. <span>This display is an exact finite illustration, not the proof.</span></footer></main>`;

const input = document.querySelector<HTMLInputElement>("#m")!;
function render(): void {
  const m = Number(input.value);
  const coefficients = widthFourCoefficients(m);
  const maximum = coefficients.reduce((best, value) => value > best ? value : best, 0n);
  const degree = coefficients.length - 1;
  document.querySelector("#m-value")!.textContent = String(m);
  document.querySelector("#formula")!.textContent = `[${m + 4} choose 4]_ℱ`;
  document.querySelector("#fib")!.textContent = `F_${m + 1}=${fibonacci(m + 1)}, F_${m + 2}=${fibonacci(m + 2)}`;
  document.querySelector("#degree")!.textContent = `Degree ${degree} · ${coefficients.length} exact coefficients`;
  const correct = isUnimodal(coefficients) && isSymmetric(coefficients);
  const verdict = document.querySelector("#verdict")!;
  verdict.textContent = correct ? "symmetric + unimodal" : "check failed";
  verdict.className = correct ? "pass" : "fail";
  document.querySelector("#chart")!.innerHTML = coefficients.map((value, index) => {
    const height = Number((value * 10000n) / maximum) / 100;
    return `<i style="height:${Math.max(1, height)}%" title="coefficient of q^${index}: ${value}"></i>`;
  }).join("");
}
input.addEventListener("input", render);render();
