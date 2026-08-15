import { createRouter, createWebHistory } from "vue-router"
import HomePage from "../pages/HomePage.vue"
import LoginPage from "../pages/LoginPage.vue"
import PostPage from "../pages/PostPage.vue"
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
      path: "/projects/",
      name: "projects",
      component: ProjectsPage,
    },
    {
      path: "/projects/:project/",
      name: "project-posts",
      component: ProjectPostsPage,
    },
    {
      path: "/projects/:project/:postNumber/",
      name: "post",
      component: PostPage,
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
