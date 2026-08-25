import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"

const caddyPageMeta = {
  name: "caddy-page-meta",
  apply: "build",
  transformIndexHtml(html) {
    return html.replace(
      "<!-- page-meta -->",
      '{{httpInclude (printf "/_api/page-meta/?path=%s" .OriginalReq.URL.Path)}}',
    )
  },
}

export default defineConfig({
  plugins: [vue(), caddyPageMeta],
  server: {
    proxy: {
      "/_api": {
        target: "http://backend:8000",
        changeOrigin: true,
      },
      "/files": {
        target: "http://backend:8000",
        changeOrigin: true,
      },
    },
  },
})
