import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"

const caddyTemplates = {
  name: "caddy-templates",
  apply: "build",
  transformIndexHtml(html) {
    return html
      .replace(
        "<!-- google-site-verification -->",
        `<meta name="google-site-verification" content='{{placeholder "env.GOOGLE_SITE_VERIFICATION"}}' />`,
      )
      .replace(
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
  plugins: [vue(), caddyTemplates],
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
