import { describe, expect, it } from "vitest";
import { isSymmetric, isUnimodal, widthFourCoefficients } from "./model";

describe("width-four q-Fibonomial coefficient generator", () => {
  it("produces symmetric unimodal coefficient sequences for displayed widths", () => {
    for (let m = 1; m <= 10; m += 1) {
      const coefficients = widthFourCoefficients(m);
      expect(coefficients.every((value) => value >= 0n)).toBe(true);
      expect(isSymmetric(coefficients)).toBe(true);
      expect(isUnimodal(coefficients)).toBe(true);
    }
  });
});
