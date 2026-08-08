import { describe, expect, it } from "vitest";
import { exactRoute, output, waterfill, type Pool } from "./model";

const pools: Pool[] = [
  { name: "A", inputReserve: 1000, outputReserve: 1200, fee: 0.997, fixedCost: 2 },
  { name: "B", inputReserve: 1600, outputReserve: 1850, fee: 0.997, fixedCost: 3 },
];
describe("small active-set AMM router", () => {
  it("preserves the input constraint and selects no worse than either one-pool route", () => {
    const allocation = waterfill(pools, 120);
    expect(allocation.reduce((sum, value) => sum + value, 0)).toBeCloseTo(120, 10);
    const route = exactRoute(pools, 120);
    expect(route.net).toBeGreaterThanOrEqual(output(pools[0]!, 120) - pools[0]!.fixedCost - 1e-10);
    expect(route.net).toBeGreaterThanOrEqual(output(pools[1]!, 120) - pools[1]!.fixedCost - 1e-10);
  });
});
