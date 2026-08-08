export function fibonacci(index: number): bigint {
  if (!Number.isInteger(index) || index < 0) throw new Error("index must be a nonnegative integer");
  let previous = 0n;
  let current = 1n;
  for (let i = 0; i < index; i += 1) [previous, current] = [current, previous + current];
  return previous;
}

function multiply(left: bigint[], right: bigint[]): bigint[] {
  const output = Array<bigint>(left.length + right.length - 1).fill(0n);
  for (let i = 0; i < left.length; i += 1) for (let j = 0; j < right.length; j += 1) output[i + j] = (output[i + j] ?? 0n) + (left[i] ?? 0n) * (right[j] ?? 0n);
  return output;
}

function divideExactly(numerator: bigint[], denominator: bigint[]): bigint[] {
  const remainder = [...numerator];
  const quotient = Array<bigint>(numerator.length - denominator.length + 1).fill(0n);
  const lead = denominator[denominator.length - 1];
  if (lead !== 1n) throw new Error("monic divisor required");
  for (let degree = quotient.length - 1; degree >= 0; degree -= 1) {
    const coefficient = remainder[degree + denominator.length - 1] ?? 0n;
    quotient[degree] = coefficient;
    for (let j = 0; j < denominator.length; j += 1) remainder[degree + j] = (remainder[degree + j] ?? 0n) - coefficient * (denominator[j] ?? 0n);
  }
  if (remainder.slice(0, denominator.length - 1).some((value) => value !== 0n)) throw new Error("division was not exact");
  return quotient;
}

function qInteger(size: bigint): bigint[] {
  if (size < 1n || size > BigInt(Number.MAX_SAFE_INTEGER)) throw new Error("displayed q-integer is too large");
  return Array<bigint>(Number(size)).fill(1n);
}

export function widthFourCoefficients(m: number): bigint[] {
  const a = fibonacci(m + 1);
  const b = fibonacci(m + 2);
  const numerator = [a, b, a + b, a + 2n * b].reduce<bigint[]>((poly, size) => multiply(poly, qInteger(size)), [1n]);
  return divideExactly(numerator, multiply(qInteger(2n), qInteger(3n)));
}

export function isUnimodal(coefficients: readonly bigint[]): boolean {
  let decreasing = false;
  for (let i = 1; i < coefficients.length; i += 1) {
    if ((coefficients[i] ?? 0n) < (coefficients[i - 1] ?? 0n)) decreasing = true;
    if (decreasing && (coefficients[i] ?? 0n) > (coefficients[i - 1] ?? 0n)) return false;
  }
  return true;
}

export function isSymmetric(coefficients: readonly bigint[]): boolean {
  return coefficients.every((value, index) => value === coefficients[coefficients.length - 1 - index]);
}
