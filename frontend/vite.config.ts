import { resolve } from "node:path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: "../pikaqiu_agent/static",
    emptyOutDir: false,
    sourcemap: false,
    rollupOptions: {
      input: {
        index: resolve(__dirname, "index.html"),
        settings: resolve(__dirname, "settings.html")
      }
    }
  },
  server: {
    proxy: {
      "/api": "http://127.0.0.1:8001"
    }
  }
});
