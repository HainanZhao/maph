import { FloatField, TwistResponseEngine, uniformProductWeights } from "../../twist-response/src/engine";

type Request = { id: number; n: number; defect: number; factor: number; tx: number; ty: number; tz: number };

function responses(n: number, tx: number, ty: number, tz: number, defect?: number, factor?: number): number[][] {
  const field = new FloatField();
  const engine = new TwistResponseEngine({
    n, field, weights: { tx, ty, tz },
    perturbHandle: defect,
    perturbFactor: factor,
  });
  return engine.sharedResponses(uniformProductWeights(field).slice(0, engine.genus));
}

self.onmessage = (event: MessageEvent<Request>) => {
  const request = event.data;
  try {
    const started = performance.now();
    const baseline = responses(request.n, request.tx, request.ty, request.tz);
    const perturbed = responses(request.n, request.tx, request.ty, request.tz, request.defect, request.factor);
    const delta = perturbed.map((row, i) => row.map((value, j) => value - (baseline[i]?.[j] ?? 0)));
    const scale = Math.max(...delta.flat().map((value) => Math.abs(value)), 1e-300);
    self.postMessage({ id: request.id, ok: true, result: { baseline, perturbed, delta, scale, elapsedMs: performance.now() - started } });
  } catch (error) {
    self.postMessage({ id: request.id, ok: false, error: error instanceof Error ? error.message : String(error) });
  }
};
