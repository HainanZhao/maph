export interface Pool { name: string; inputReserve: number; outputReserve: number; fee: number; fixedCost: number; }
export interface Route { allocation: number[]; gross: number; fixed: number; net: number; active: number[]; }

export function output(pool: Pool, input: number): number {
  const effective = pool.fee * input;
  return pool.outputReserve * effective / (pool.inputReserve + effective);
}
function marginal(pool: Pool): number { return pool.outputReserve * pool.fee / pool.inputReserve; }

export function waterfill(pools: readonly Pool[], amount: number): number[] {
  let active = pools.map((_, index) => index);
  while (true) {
    const numerator = active.reduce((sum, index) => sum + Math.sqrt(pools[index]!.inputReserve * pools[index]!.outputReserve * pools[index]!.fee) / pools[index]!.fee, 0);
    const denominator = amount + active.reduce((sum, index) => sum + pools[index]!.inputReserve / pools[index]!.fee, 0);
    const sharedMarginal = (numerator / denominator) ** 2;
    const reduced = active.filter((index) => marginal(pools[index]!) > sharedMarginal);
    if (reduced.length === active.length) {
      const allocation = pools.map(() => 0);
      active.forEach((index) => { allocation[index] = (Math.sqrt(pools[index]!.inputReserve * pools[index]!.outputReserve * pools[index]!.fee / sharedMarginal) - pools[index]!.inputReserve) / pools[index]!.fee; });
      const largest = active.reduce((best, index) => (allocation[index] ?? 0) > (allocation[best] ?? 0) ? index : best);
      allocation[largest] = (allocation[largest] ?? 0) + amount - allocation.reduce((sum, value) => sum + value, 0);
      return allocation;
    }
    active = reduced.length ? reduced : [active.reduce((best, index) => marginal(pools[index]!) > marginal(pools[best]!) ? index : best)];
  }
}

export function evaluate(pools: readonly Pool[], allocation: readonly number[]): Route {
  const gross = pools.reduce((sum, pool, index) => sum + output(pool, allocation[index] ?? 0), 0);
  const active = allocation.flatMap((value, index) => value > 1e-10 ? [index] : []);
  const fixed = active.reduce((sum, index) => sum + pools[index]!.fixedCost, 0);
  return { allocation: [...allocation], gross, fixed, net: gross - fixed, active };
}

export function exactRoute(pools: readonly Pool[], amount: number): Route {
  let best: Route | null = null;
  for (let mask = 1; mask < 1 << pools.length; mask += 1) {
    const selected = pools.flatMap((pool, index) => mask & (1 << index) ? [pool] : []);
    const selectedIndices = pools.flatMap((_, index) => mask & (1 << index) ? [index] : []);
    const local = waterfill(selected, amount);
    const allocation = pools.map(() => 0);
    selectedIndices.forEach((index, localIndex) => { allocation[index] = local[localIndex] ?? 0; });
    const candidate = evaluate(pools, allocation);
    if (!best || candidate.net > best.net) best = candidate;
  }
  if (!best) throw new Error("at least one pool is required");
  return best;
}
