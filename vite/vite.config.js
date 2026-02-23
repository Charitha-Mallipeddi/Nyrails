import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  base: "/static/",
  resolve: {
    alias: {
      '@font': resolve('./core/static/fonts'),
    },
  },
  build: {

    manifest: "manifest.json",
    outDir: resolve("./assets"),
    rollupOptions: {
      input: {
        "vendors": resolve('./core/static/js/vendors.js')
      }
    }
  }
})
