import { resolve } from "node:path";
import { defineConfig } from "vite";

export default defineConfig({
  base: process.env.BASE_PATH ?? "/",
  build: {
    target: "es2022",
    rollupOptions: {
      input: {
        home: resolve(import.meta.dirname, "index.html"),
        isingTwistResponse: resolve(import.meta.dirname, "three-dimensional-ising/twist-response/index.html"),
      },
    },
  },
});
