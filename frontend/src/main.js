import { createApp } from "vue"
import "@fontsource/ibm-plex-mono/cyrillic-400.css"
import "@fontsource/ibm-plex-mono/latin-400.css"
import "@fontsource/ibm-plex-mono/cyrillic-600.css"
import "@fontsource/ibm-plex-mono/latin-600.css"
import "@fontsource/ibm-plex-mono/cyrillic-700.css"
import "@fontsource/ibm-plex-mono/latin-700.css"
import "@fontsource-variable/sofia-sans/wght.css"
import "@fontsource-variable/sofia-sans/wght-italic.css"
import App from "./App.vue"
import router from "./router"
import { setDefaultPageMeta } from "./utils/pageMeta.js"
import "./style.css"

router.afterEach((to) => setDefaultPageMeta(to.name))

createApp(App).use(router).mount("#app")
