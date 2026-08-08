import "./hub.css";
import { DEMOS } from "./catalog";

const app = document.querySelector<HTMLDivElement>("#app");
if (!app) throw new Error("missing app root");

const projectCount = new Set(DEMOS.map((demo) => demo.project)).size;
app.innerHTML = `
  <header>
    <nav><a href="https://github.com/HainanZhao/maph">maph / github</a><span>${projectCount} project · ${DEMOS.length} live demo</span></nav>
    <p class="eyebrow">Mathematics you can touch</p>
    <h1>Research demos,<br><i>not result theatre.</i></h1>
    <p class="lede">Each page exposes a real algorithm, certificate, or structural obstruction from the underlying project. Measured data and extrapolations are labelled separately.</p>
  </header>
  <main>
    <div class="rule"><span>Interactive projects</span><b>${String(DEMOS.length).padStart(2, "0")}</b></div>
    <section class="cards">${DEMOS.map((demo, index) => `
      <a class="card" href="${demo.path}" style="--accent:${demo.accent}">
        <div class="card-top"><span>${String(index + 1).padStart(2, "0")}</span><code>${demo.status}</code></div>
        <p>${demo.projectLabel}</p><h2>${demo.title}</h2><div class="description">${demo.description}</div>
        <div class="open">Open demonstration <b>↗</b></div>
      </a>`).join("")}</section>
  </main>
  <footer><span>Hainan Zhao</span><span>Exact claims state their validation boundary.</span></footer>`;
