import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"

const caddyPageMeta = {
  name: "caddy-page-meta",
  apply: "build",
  transformIndexHtml(html) {
    return html.replace(
      "<!-- page-meta -->",
      `{{if eq (placeholder "http.error.status_code") "404"}}
      <title data-page-meta>Страница не найдена</title>
      <meta name="robots" content="noindex" data-page-meta>
      {{else}}
      {{httpInclude (printf "/_api/page-meta/?path=%s" .OriginalReq.URL.Path)}}
      {{end}}`,
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
