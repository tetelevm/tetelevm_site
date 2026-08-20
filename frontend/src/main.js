import { createApp } from "vue"
import App from "./App.vue"
import router from "./router"
import "./style.css"

document.title = import.meta.env.PROD ? "tetelevm" : "tetelevm.dev"

createApp(App).use(router).mount("#app")
