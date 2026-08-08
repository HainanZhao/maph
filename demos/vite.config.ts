import { resolve } from "node:path";
import { defineConfig } from "vite";

export default defineConfig({
  base: process.env.BASE_PATH ?? "/",
  build: {
    target: "es2022",
    rollupOptions: {
      input: {
        home: resolve(import.meta.dirname, "index.html"),
        gridPhaseClosure: resolve(import.meta.dirname, "certifiable-grid-optimization/phase-closure/index.html"),
        ammRouteLaboratory: resolve(import.meta.dirname, "gas-aware-amm-routing/route-laboratory/index.html"),
        qfibMountain: resolve(import.meta.dirname, "open-conjecture-sweep/qfib-mountain/index.html"),
        isingDefectLaboratory: resolve(import.meta.dirname, "three-dimensional-ising/defect-laboratory/index.html"),
        isingTwistResponse: resolve(import.meta.dirname, "three-dimensional-ising/twist-response/index.html"),
      },
    },
  },
});
