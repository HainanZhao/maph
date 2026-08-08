export interface DemoEntry {
  project: string;
  projectLabel: string;
  title: string;
  description: string;
  path: string;
  status: "PROVED" | "CERTIFIED_NUMERICAL" | "OBSERVED" | "EXPLORATORY";
  accent: string;
}

// Add one record for each public page. Each project may register multiple
// independent demos without changing the build or deployment workflow.
export const DEMOS: DemoEntry[] = [
  {
    project: "certifiable-grid-optimization",
    projectLabel: "Power-grid certificates",
    title: "Can Local Grid Readings Fit One Grid?",
    description: "An exact three-bus cycle-closure certificate distinguishes locally plausible line data from one globally consistent voltage assignment.",
    path: "certifiable-grid-optimization/phase-closure/",
    status: "PROVED",
    accent: "#3b9a69",
  },
  {
    project: "gas-aware-amm-routing",
    projectLabel: "AMM routing",
    title: "When Is Another Route Worth Its Gas?",
    description: "An exact small-instance active-set control makes the trade-off between better prices and fixed execution costs tangible.",
    path: "gas-aware-amm-routing/route-laboratory/",
    status: "OBSERVED",
    accent: "#69c985",
  },
  {
    project: "open-conjecture-sweep",
    projectLabel: "q-Fibonomials",
    title: "The q-Fibonomial Mountain",
    description: "Exact integer coefficient profiles make a proved infinite unimodality theorem visible, one width-four polynomial at a time.",
    path: "open-conjecture-sweep/qfib-mountain/",
    status: "PROVED",
    accent: "#df6c3b",
  },
  {
    project: "three-dimensional-ising",
    projectLabel: "Three-dimensional Ising",
    title: "One Defect, Every Response",
    description: "Perturb one local coupling in a 3×3×n Ising strip and map every all-sector handle response through the exact 256-state carrier.",
    path: "three-dimensional-ising/defect-laboratory/",
    status: "OBSERVED",
    accent: "#e0654a",
  },
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
