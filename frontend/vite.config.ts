import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: "dist", // Default build output folder
  },
  server: {
    proxy: {
      "/api": "http://localhost:8000",
      "/analyze": "http://localhost:8000",
    },
  },
});
