export const TAU = 2 * Math.PI;
export function wrap(angle: number): number {
  let value = (angle + Math.PI) % TAU;
  if (value < 0) value += TAU;
  return value - Math.PI;
}
export function cycleDefect(edges: readonly number[]): number {
  if (edges.length !== 3) throw new Error("a triangle requires three oriented edge phases");
  return wrap(edges.reduce((sum, edge) => sum + edge, 0));
}
export function reconstruct(edges: readonly number[]): number[] {
  const [a, b] = edges;
  if (a === undefined || b === undefined) throw new Error("missing edge phase");
  return [0, a, a + b];
}
