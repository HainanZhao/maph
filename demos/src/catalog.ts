export interface DemoEntry {
  project: string;
  projectLabel: string;
  title: string;
  description: string;
  path: string;
  status: "PROVED" | "CERTIFIED_NUMERICAL" | "EXPLORATORY";
  accent: string;
}

// Add one record for each public page. Each project may register multiple
// independent demos without changing the build or deployment workflow.
export const DEMOS: DemoEntry[] = [
  {
    project: "three-dimensional-ising",
    projectLabel: "Three-dimensional Ising",
    title: "Where Did the 4^g Ising Sectors Go?",
    description: "An exact 256-state twist-response engine for 3×3×n cubic-lattice strips, with shared-environment marginals and reproducible benchmarks.",
    path: "three-dimensional-ising/twist-response/",
    status: "CERTIFIED_NUMERICAL",
    accent: "#ee7052",
  },
];
