import {
  BOND,
  FloatField,
  PrimeField,
  PRIMES,
  TwistResponseEngine,
  responseTablesEqual,
  uniformProductWeights,
} from "./engine";

type Request =
  | { id: number; type: "calculate"; n: number; tx: number; ty: number; tz: number; perturbHandle: number; perturbFactor: number }
  | { id: number; type: "exact"; n: number }
  | { id: number; type: "benchmark"; tx: number; ty: number; tz: number };

function now(): number { return performance.now(); }

function floatEngine(n: number, tx: number, ty: number, tz: number, perturbHandle = -1, perturbFactor = 1) {
  const field = new FloatField();
  return {
    field,
    engine: new TwistResponseEngine({
      n,
      field,
      weights: { tx, ty, tz },
      perturbHandle: perturbHandle >= 0 ? perturbHandle : undefined,
      perturbFactor: perturbHandle >= 0 ? perturbFactor : undefined,
    }),
  };
}

function calculate(request: Extract<Request, { type: "calculate" }>) {
  const { field, engine } = floatEngine(request.n, request.tx, request.ty, request.tz, request.perturbHandle, request.perturbFactor);
  const product = uniformProductWeights(field).slice(0, engine.genus);
  const started = now();
  const responses = engine.sharedResponses(product);
  const elapsedMs = now() - started;
  const arfWeights = Array.from({ length: engine.genus }, () => [1, 1, 1, -1]);
  const arfSum = engine.contractProduct(arfWeights);
  return { responses, elapsedMs, arfSum, genus: engine.genus, sectors: `4^${engine.genus}` };
}

function exact(request: Extract<Request, { type: "exact" }>) {
  const n = Math.min(7, Math.max(2, request.n));
  return PRIMES.map((prime) => {
    const field = new PrimeField(prime);
    const engine = new TwistResponseEngine({ n, field, weights: { tx: 2n, ty: 3n, tz: 5n } });
    const product = uniformProductWeights(field).slice(0, engine.genus);
    const sharedStart = now();
    const shared = engine.sharedResponses(product);
    const sharedMs = now() - sharedStart;
    const literalStart = now();
    const literal = engine.literalResponses(product);
    const literalMs = now() - literalStart;
    return {
      prime: prime.toString(),
      n,
      sharedMs,
      literalMs,
      agrees: responseTablesEqual(shared, literal),
      checksum: shared.flat().reduce((acc, value) => (acc * 65537n + value) % prime, 0n).toString(),
    };
  });
}

function denseMatVec(matrix: number[][], vector: number[]): number[] {
  return matrix.map((row) => row.reduce((sum, value, column) => sum + value * (vector[column] ?? 0), 0));
}

function benchmark(request: Extract<Request, { type: "benchmark" }>) {
  const sharedRows = [];
  for (const n of [2, 4, 7, 10, 20, 50, 100]) {
    const { field, engine } = floatEngine(n, request.tx, request.ty, request.tz);
    const product = uniformProductWeights(field).slice(0, engine.genus);
    const started = now();
    engine.sharedResponses(product);
    sharedRows.push({ n, ms: now() - started, measured: true });
  }

  const comparisonRows = [];
  for (const n of [2, 4, 7, 10]) {
    const { field, engine } = floatEngine(n, request.tx, request.ty, request.tz);
    const product = uniformProductWeights(field).slice(0, engine.genus);
    const sharedStart = now();
    engine.sharedResponses(product);
    const sharedMs = now() - sharedStart;
    const separateStart = now();
    engine.separateResponses(product);
    const separateMs = now() - separateStart;
    comparisonRows.push({ n, sharedMs, separateMs, speedup: separateMs / Math.max(sharedMs, 1e-9) });
  }

  const literalRows = [];
  for (const n of [2, 3, 4, 5]) {
    const { field, engine } = floatEngine(n, request.tx, request.ty, request.tz);
    const product = uniformProductWeights(field).slice(0, engine.genus);
    const started = now();
    engine.literalResponses(product);
    literalRows.push({ n, ms: now() - started, sectors: 4 ** engine.genus, measured: true });
  }

  const { engine } = floatEngine(8, request.tx, request.ty, request.tz);
  const vector = Array.from({ length: BOND }, (_, i) => 0.5 + ((i * 37) % 101) / 101);
  const structuredStart = now();
  let structured = vector;
  for (let repeat = 0; repeat < 8; repeat += 1) structured = engine.applyCore(structured, 3, 0);
  const structuredMs = (now() - structuredStart) / 8;
  const constructionStart = now();
  const dense = engine.materializeCore(3, 0);
  const denseConstructionMs = now() - constructionStart;
  const denseStart = now();
  let denseResult = vector;
  for (let repeat = 0; repeat < 8; repeat += 1) denseResult = denseMatVec(dense, denseResult);
  const denseMs = (now() - denseStart) / 8;
  const maxDifference = Math.max(...structured.map((value, i) => Math.abs(value - (denseResult[i] ?? 0))));

  return {
    generatedAt: new Date().toISOString(),
    weights: { tx: request.tx, ty: request.ty, tz: request.tz },
    sharedRows,
    comparisonRows,
    literalRows,
    coreApplication: {
      structuredMs,
      denseMs,
      denseConstructionMs,
      maxDifference,
      oneDenseCoreBytes: BOND * BOND * 8,
      allDenseCoresAtN100Bytes: 4 * 99 * BOND * BOND * 8,
      structuredStateBytes: BOND * 8,
    },
    note: "Literal rows are measured only through n=5; larger literal costs must be shown as extrapolations.",
  };
}

self.onmessage = (event: MessageEvent<Request>) => {
  const request = event.data;
  try {
    const result = request.type === "calculate" ? calculate(request)
      : request.type === "exact" ? exact(request)
        : benchmark(request);
    self.postMessage({ id: request.id, ok: true, result });
  } catch (error) {
    self.postMessage({ id: request.id, ok: false, error: error instanceof Error ? error.message : String(error) });
  }
};
