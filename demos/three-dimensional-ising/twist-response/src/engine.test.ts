import { describe, expect, it } from "vitest";
import {
  FloatField,
  PrimeField,
  PRIMES,
  TwistResponseEngine,
  responseTablesEqual,
  uniformProductWeights,
} from "./engine";
import reference from "../fixtures/reference.json";

const FIXTURES: Record<string, Record<number, number[][]>> = {
  "1000000007": {
    2: [[293716784, 888543660, 533722126, 244551209]],
    3: [[111722382, 948962079, 760894624, 849715860], [111722382, 948962079, 760894624, 849715860]],
    4: [[203054918, 414429287, 280573989, 42678988], [203054918, 608815986, 791224916, 81928477], [203054918, 414429287, 736457092, 349865874]],
  },
  "1000000009": {
    2: [[256792016, 885078420, 515994642, 246710983]],
    3: [[906146549, 750252430, 291691092, 939582597], [906146549, 750252430, 291691092, 939582597]],
    4: [[911440076, 940666269, 5880921, 245775627], [911440076, 630100553, 310058374, 46098360], [911440076, 940666269, 379426088, 328819683]],
  },
};

describe("width-three twist-response engine", () => {
  it("matches all independent n=2..7 regime checksums", () => {
    for (const row of reference.rows) {
      const prime = BigInt(row.prime);
      const field = new PrimeField(prime);
      const nonuniform = row.regime === "nonuniform";
      const weights = row.regime === "isotropic"
        ? { tx: 2n, ty: 2n, tz: 2n }
        : { tx: 2n, ty: 3n, tz: 5n };
      const engine = new TwistResponseEngine({
        n: row.n,
        field,
        weights,
        gateWeight: nonuniform
          ? (layer, flip) => BigInt(2 + ((layer + 1) * 1009 + flip * 9176) % 9973)
          : undefined,
        connectorSiteWeight: nonuniform
          ? (layer, site) => BigInt(2 + ((layer + 1) * 1237 + (site + 1) * 733) % 9973)
          : undefined,
      });
      const responses = engine.sharedResponses(uniformProductWeights(field).slice(0, engine.genus));
      const checksum = responses.flat().reduce((acc, value) => (acc * 65537n + value) % prime, 0n);
      expect(checksum, `${row.regime}, n=${row.n}, p=${row.prime}`).toBe(BigInt(row.response_checksum));
    }
  }, 30_000);

  it("matches the independent Python core fixtures over both primes", () => {
    for (const prime of PRIMES) {
      for (const n of [2, 3, 4]) {
        const field = new PrimeField(prime);
        const engine = new TwistResponseEngine({ n, field, weights: { tx: 2n, ty: 3n, tz: 5n } });
        const observed = engine.sharedResponses(uniformProductWeights(field).slice(0, n - 1));
        const expected = FIXTURES[prime.toString()]?.[n]?.map((row) => row.map(BigInt));
        expect(observed).toEqual(expected);
      }
    }
  });

  it("shared, separate, and literal contractions agree exactly", () => {
    const field = new PrimeField(PRIMES[0]);
    for (const n of [2, 3, 4]) {
      const engine = new TwistResponseEngine({ n, field, weights: { tx: 7n, ty: 11n, tz: 13n } });
      const weights = uniformProductWeights(field).slice(0, n - 1);
      const shared = engine.sharedResponses(weights);
      expect(responseTablesEqual(shared, engine.separateResponses(weights))).toBe(true);
      expect(responseTablesEqual(shared, engine.literalResponses(weights))).toBe(true);
    }
  });

  it("retains exact agreement after one local coupling perturbation", () => {
    const field = new PrimeField(PRIMES[1]);
    const engine = new TwistResponseEngine({
      n: 5,
      field,
      weights: { tx: 7n, ty: 11n, tz: 13n },
      perturbHandle: 2,
      perturbFactor: 17n,
    });
    const weights = uniformProductWeights(field).slice(0, engine.genus);
    const shared = engine.sharedResponses(weights);
    expect(responseTablesEqual(shared, engine.separateResponses(weights))).toBe(true);
    expect(responseTablesEqual(shared, engine.literalResponses(weights))).toBe(true);
  });

  it("floating-point paths agree within roundoff", () => {
    const field = new FloatField();
    const engine = new TwistResponseEngine({ n: 4, field, weights: { tx: 0.19, ty: 0.23, tz: 0.17 } });
    const weights = uniformProductWeights(field).slice(0, 3);
    const shared = engine.sharedResponses(weights);
    const literal = engine.literalResponses(weights);
    for (let i = 0; i < shared.length; i += 1) {
      for (let c = 0; c < 4; c += 1) {
        const scale = Math.max(1, Math.abs(literal[i]?.[c] ?? 0));
        expect(Math.abs((shared[i]?.[c] ?? 0) - (literal[i]?.[c] ?? 0)) / scale).toBeLessThan(1e-11);
      }
    }
  });

  it("keeps the advertised n=100 floating-point workload finite", () => {
    const field = new FloatField();
    const engine = new TwistResponseEngine({ n: 100, field, weights: { tx: 0.3, ty: 0.3, tz: 0.3 } });
    const responses = engine.sharedResponses(uniformProductWeights(field).slice(0, engine.genus));
    expect(responses).toHaveLength(99);
    expect(responses.flat().every(Number.isFinite)).toBe(true);
  }, 15_000);
});
