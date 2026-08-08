export const WIDTH = 3;
export const MASK_BITS = WIDTH * WIDTH;
export const BOND = 1 << (MASK_BITS - 1);
export const PRIMES = [1_000_000_007n, 1_000_000_009n] as const;

export type AxisWeights<T> = { tx: T; ty: T; tz: T };
export type ResponseTable<T> = T[][];

export interface Field<T> {
  readonly zero: T;
  readonly one: T;
  add(a: T, b: T): T;
  mul(a: T, b: T): T;
  neg(a: T): T;
  inv2(): T;
}

export class FloatField implements Field<number> {
  readonly zero = 0;
  readonly one = 1;
  add(a: number, b: number): number { return a + b; }
  mul(a: number, b: number): number { return a * b; }
  neg(a: number): number { return -a; }
  inv2(): number { return 0.5; }
}

export class PrimeField implements Field<bigint> {
  readonly zero = 0n;
  readonly one = 1n;
  constructor(readonly prime: bigint) {}
  add(a: bigint, b: bigint): bigint {
    const value = a + b;
    return value >= this.prime ? value - this.prime : value;
  }
  mul(a: bigint, b: bigint): bigint { return (a * b) % this.prime; }
  neg(a: bigint): bigint { return a === 0n ? 0n : this.prime - a; }
  inv2(): bigint { return (this.prime + 1n) / 2n; }
}

const GAUSS = [
  [1, 1, 1, -1],
  [1, 1, -1, 1],
  [1, -1, 1, 1],
  [-1, 1, 1, 1],
] as const;

const FLIPS = [3, 9, 6, 18, 36, 24, 72, 48, 144, 288, 192, 384] as const;
const START_LEADING = new Set([384]);
const EVEN_LEADING = new Set([72, 144]);
const ODD_LEADING = new Set([24, 192]);
const EVEN_TRAILING = new Set([6, 48]);
const ODD_TRAILING = new Set([18, 36]);

const EVEN_MASKS = Array.from({ length: 1 << MASK_BITS }, (_, mask) => mask)
  .filter((mask) => popcount(mask) % 2 === 0);
const MASK_INDEX = new Map(EVEN_MASKS.map((mask, index) => [mask, index]));
const ZERO_INDEX = MASK_INDEX.get(0) ?? 0;
const PERMUTATIONS = new Map<number, number[]>(
  FLIPS.map((flip) => [flip, EVEN_MASKS.map((mask) => MASK_INDEX.get(mask ^ flip) ?? -1)]),
);

function popcount(value: number): number {
  let count = 0;
  for (let x = value; x; x &= x - 1) count += 1;
  return count;
}

function parity(value: number): number { return popcount(value) & 1; }

function axisForFlip(flip: number): "ty" | "tz" {
  const sites: number[] = [];
  for (let bit = 0; bit < MASK_BITS; bit += 1) if ((flip >> bit) & 1) sites.push(bit);
  if (sites.length !== 2) throw new Error(`invalid parity flip ${flip}`);
  return Math.abs((sites[0] ?? 0) - (sites[1] ?? 0)) === 1 ? "tz" : "ty";
}

function filled<T>(value: T): T[] { return Array.from({ length: BOND }, () => value); }

function addVectors<T>(field: Field<T>, target: T[], source: T[], coefficient: T): void {
  for (let i = 0; i < BOND; i += 1) {
    target[i] = field.add(target[i] as T, field.mul(coefficient, source[i] as T));
  }
}

export interface EngineOptions<T> {
  n: number;
  field: Field<T>;
  weights: AxisWeights<T>;
  perturbHandle?: number;
  perturbFactor?: T;
  gateWeight?: (layer: number, flip: number) => T;
  connectorSiteWeight?: (layer: number, site: number) => T;
}

export class TwistResponseEngine<T> {
  readonly genus: number;
  readonly edgeTransitions = FLIPS.length;
  constructor(readonly options: EngineOptions<T>) {
    if (!Number.isInteger(options.n) || options.n < 2) throw new Error("n must be an integer at least two");
    this.genus = options.n - 1;
  }

  boundaryVector(): T[] {
    const vector = filled(this.options.field.zero);
    vector[ZERO_INDEX] = this.options.field.one;
    return vector;
  }

  private weightForFlip(flip: number, group: number, stage: "leading" | "trailing"): T {
    const { field, weights, perturbHandle, perturbFactor, gateWeight } = this.options;
    let weight = gateWeight ? gateWeight(stage === "leading" ? group : group + 1, flip) : weights[axisForFlip(flip)];
    if (group === perturbHandle && perturbFactor !== undefined) weight = field.mul(weight, perturbFactor);
    return weight;
  }

  private connectorWeight(group: number, site: number): T {
    const { field, weights, perturbHandle, perturbFactor, connectorSiteWeight } = this.options;
    if (connectorSiteWeight) return connectorSiteWeight(group, site);
    return group === perturbHandle && perturbFactor !== undefined
      ? field.mul(weights.tx, perturbFactor)
      : weights.tx;
  }

  private leadingSet(group: number): Set<number> {
    if (group === 0) return START_LEADING;
    return group % 2 === 0 ? EVEN_LEADING : ODD_LEADING;
  }

  private leadingFlips(group: number): readonly number[] {
    if (group === 0) return FLIPS;
    const emittedByPrevious = group % 2 === 1 ? EVEN_TRAILING : ODD_TRAILING;
    return FLIPS.filter((flip) => !emittedByPrevious.has(flip));
  }

  private trailingSet(group: number): Set<number> {
    if (group === this.genus - 1) return this.leadingSet(group);
    return group % 2 === 0 ? EVEN_TRAILING : ODD_TRAILING;
  }

  private applyGate(vector: T[], flip: number, coefficient: T): T[] {
    const field = this.options.field;
    const permutation = PERMUTATIONS.get(flip);
    if (!permutation) throw new Error(`missing permutation ${flip}`);
    const result = filled(field.zero);
    for (let i = 0; i < BOND; i += 1) {
      result[i] = field.add(vector[i] as T, field.mul(coefficient, vector[permutation[i] as number] as T));
    }
    return result;
  }

  private applyGates(vector: T[], flips: readonly number[], signed: Set<number>, mu: number, group: number, stage: "leading" | "trailing", reverse = false): T[] {
    let result = vector;
    const ordered = reverse ? [...flips].reverse() : flips;
    for (const flip of ordered) {
      let coefficient = this.weightForFlip(flip, group, stage);
      if (signed.has(flip) && (mu & 1)) coefficient = this.options.field.neg(coefficient);
      result = this.applyGate(result, flip, coefficient);
    }
    return result;
  }

  private applyConnector(vector: T[], group: number): T[] {
    const field = this.options.field;
    if (!this.options.connectorSiteWeight) {
      const weight = this.connectorWeight(group, 0);
      const powers = [field.one];
      for (let i = 1; i <= MASK_BITS; i += 1) powers.push(field.mul(powers[i - 1] as T, weight));
      return vector.map((value, index) => field.mul(value, powers[popcount(EVEN_MASKS[index] as number)] as T));
    }
    return vector.map((value, index) => {
      let diagonal = field.one;
      const mask = EVEN_MASKS[index] as number;
      for (let site = 0; site < MASK_BITS; site += 1) if ((mask >> site) & 1) diagonal = field.mul(diagonal, this.connectorWeight(group, site));
      return field.mul(value, diagonal);
    });
  }

  private jumpPotentials(group: number): [number | null, number] {
    const last = group === this.genus - 1;
    if (group === 0) return [last ? null : 292, 432];
    if (group % 2 === 0) return [last ? null : 484, 432];
    return [last ? null : 432, 484];
  }

  private applyJump(vector: T[], group: number, mu: number): T[] {
    const field = this.options.field;
    const [aPotential, bPotential] = this.jumpPotentials(group);
    let potential = 0;
    if ((mu & 1) && aPotential !== null) potential ^= aPotential;
    if (mu & 2) potential ^= bPotential;
    if (!potential) return vector;
    return vector.map((value, index) => parity((EVEN_MASKS[index] as number) & potential) ? field.neg(value) : value);
  }

  applyCharacterBlock(vector: T[], group: number, mu: number, transpose = false): T[] {
    const leading = this.leadingFlips(group);
    const trailing = group === this.genus - 1 ? FLIPS : [...this.trailingSet(group)];
    if (!transpose) {
      let result = this.applyGates(vector, leading, this.leadingSet(group), mu, group, "leading");
      result = this.applyConnector(result, group);
      result = this.applyJump(result, group, mu);
      return this.applyGates(result, trailing, this.trailingSet(group), mu, group, "trailing");
    }
    let result = this.applyGates(vector, trailing, this.trailingSet(group), mu, group, "trailing", true);
    result = this.applyJump(result, group, mu);
    result = this.applyConnector(result, group);
    return this.applyGates(result, leading, this.leadingSet(group), mu, group, "leading", true);
  }

  applyCore(vector: T[], group: number, state: number, transpose = false): T[] {
    const field = this.options.field;
    const result = filled(field.zero);
    for (let mu = 0; mu < 4; mu += 1) {
      const transformed = this.applyCharacterBlock(vector, group, mu, transpose);
      const signed = GAUSS[state]?.[mu] === -1 ? field.neg(field.one) : field.one;
      addVectors(field, result, transformed, signed);
    }
    const half = field.inv2();
    return result.map((value) => field.mul(value, half));
  }

  applyWeighted(vector: T[], group: number, weights: readonly T[], transpose = false): T[] {
    const field = this.options.field;
    const result = filled(field.zero);
    for (let state = 0; state < 4; state += 1) {
      addVectors(field, result, this.applyCore(vector, group, state, transpose), weights[state] as T);
    }
    return result;
  }

  evaluateSector(states: readonly number[]): T {
    if (states.length !== this.genus) throw new Error("sector length mismatch");
    let vector = this.boundaryVector();
    for (let group = 0; group < this.genus; group += 1) vector = this.applyCore(vector, group, states[group] as number);
    return vector[ZERO_INDEX] as T;
  }

  contractProduct(productWeights: readonly (readonly T[])[]): T {
    let vector = this.boundaryVector();
    for (let group = 0; group < this.genus; group += 1) vector = this.applyWeighted(vector, group, productWeights[group] as readonly T[]);
    return vector[ZERO_INDEX] as T;
  }

  sharedResponses(productWeights: readonly (readonly T[])[]): ResponseTable<T> {
    const field = this.options.field;
    if (productWeights.length !== this.genus) throw new Error("product-weight length mismatch");
    const left: T[][] = [this.boundaryVector()];
    for (let i = 0; i < this.genus; i += 1) left.push(this.applyWeighted(left[i] as T[], i, productWeights[i] as readonly T[]));
    const right: T[][] = Array.from({ length: this.genus + 1 }, () => [] as T[]);
    right[this.genus] = this.boundaryVector();
    for (let i = this.genus - 1; i >= 0; i -= 1) right[i] = this.applyWeighted(right[i + 1] as T[], i, productWeights[i] as readonly T[], true);
    const answer: T[][] = [];
    for (let i = 0; i < this.genus; i += 1) {
      const fixed = Array.from({ length: 4 }, () => field.zero);
      for (let state = 0; state < 4; state += 1) {
        const middle = this.applyCore(left[i] as T[], i, state);
        let value = field.zero;
        for (let mask = 0; mask < BOND; mask += 1) value = field.add(value, field.mul(middle[mask] as T, (right[i + 1] as T[])[mask] as T));
        fixed[state] = value;
      }
      answer.push(Array.from({ length: 4 }, (_, character) => {
        let value = field.zero;
        for (let state = 0; state < 4; state += 1) {
          const term = parity(character & state) ? field.neg(fixed[state] as T) : fixed[state] as T;
          value = field.add(value, term);
        }
        return value;
      }));
    }
    return answer;
  }

  separateResponses(productWeights: readonly (readonly T[])[]): ResponseTable<T> {
    const field = this.options.field;
    return Array.from({ length: this.genus }, (_, held) => Array.from({ length: 4 }, (_, character) => {
      let response = field.zero;
      for (let state = 0; state < 4; state += 1) {
        let vector = this.boundaryVector();
        for (let group = 0; group < this.genus; group += 1) {
          vector = group === held
            ? this.applyCore(vector, group, state)
            : this.applyWeighted(vector, group, productWeights[group] as readonly T[]);
        }
        const term = parity(character & state) ? field.neg(vector[ZERO_INDEX] as T) : vector[ZERO_INDEX] as T;
        response = field.add(response, term);
      }
      return response;
    }));
  }

  literalResponses(productWeights: readonly (readonly T[])[]): ResponseTable<T> {
    const field = this.options.field;
    if (this.genus > 6) throw new Error("literal enumeration is intentionally capped at n=7");
    const answer = Array.from({ length: this.genus }, () => Array.from({ length: 4 }, () => field.zero));
    const sectorCount = 4 ** this.genus;
    for (let index = 0; index < sectorCount; index += 1) {
      const states = Array.from({ length: this.genus }, (_, i) => Math.floor(index / (4 ** i)) & 3);
      const value = this.evaluateSector(states);
      for (let held = 0; held < this.genus; held += 1) {
        let factor = value;
        for (let i = 0; i < this.genus; i += 1) if (i !== held) factor = field.mul(factor, productWeights[i]?.[states[i] as number] as T);
        for (let character = 0; character < 4; character += 1) {
          const term = parity(character & (states[held] as number)) ? field.neg(factor) : factor;
          answer[held]![character] = field.add(answer[held]?.[character] as T, term);
        }
      }
    }
    return answer;
  }

  materializeCore(group: number, state: number): T[][] {
    const columns: T[][] = [];
    for (let column = 0; column < BOND; column += 1) {
      const basis = filled(this.options.field.zero);
      basis[column] = this.options.field.one;
      columns.push(this.applyCore(basis, group, state));
    }
    return Array.from({ length: BOND }, (_, row) => columns.map((column) => column[row] as T));
  }
}

export function uniformProductWeights<T>(field: Field<T>): T[][] {
  return Array.from({ length: 100 }, () => [field.one, field.one, field.one, field.one]);
}

export function responseTablesEqual<T>(left: ResponseTable<T>, right: ResponseTable<T>): boolean {
  return left.length === right.length && left.every((row, i) => row.every((value, j) => value === right[i]?.[j]));
}
