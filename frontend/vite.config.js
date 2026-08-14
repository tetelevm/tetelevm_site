import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      "/_api": {
        target: "http://backend:8000",
        changeOrigin: true,
      },
    },
  },
})
