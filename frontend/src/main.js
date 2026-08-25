import { createApp } from "vue"
import App from "./App.vue"
import router from "./router"
import { setDefaultPageMeta } from "./utils/pageMeta.js"
import "./style.css"

router.afterEach((to) => setDefaultPageMeta(to.name))

createApp(App).use(router).mount("#app")
