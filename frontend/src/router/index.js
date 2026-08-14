import { createRouter, createWebHistory } from "vue-router"
import HomePage from "../pages/HomePage.vue"
import LoginPage from "../pages/LoginPage.vue"
import ProjectPostsPage from "../pages/ProjectPostsPage.vue"
import ProjectsPage from "../pages/ProjectsPage.vue"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomePage,
    },
    {
      path: "/content/",
      name: "projects",
      component: ProjectsPage,
    },
    {
      path: "/content/:project/",
      name: "project-posts",
      component: ProjectPostsPage,
    },
    {
      path: "/login/",
      name: "login",
      component: LoginPage,
    },
    {
      path: "/:pathMatch(.*)*",
      redirect: "/",
    },
  ],
})

export default router
