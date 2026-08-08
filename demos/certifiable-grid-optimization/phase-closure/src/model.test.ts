import { describe, expect, it } from "vitest";
import { cycleDefect, reconstruct, wrap } from "./model";

describe("cycle phase certificate", () => {
  it("recognizes a closed oriented triangle", () => {
    expect(cycleDefect([0.25, -0.1, -0.15])).toBeCloseTo(0, 12);
    expect(reconstruct([0.25, -0.1, -0.15])).toEqual([0, 0.25, 0.15]);
  });
  it("uses a principal wrapped defect", () => {
    expect(wrap(3 * Math.PI)).toBeCloseTo(-Math.PI, 12);
    expect(cycleDefect([0.25, -0.1, -0.1])).toBeCloseTo(0.05, 12);
  });
});
