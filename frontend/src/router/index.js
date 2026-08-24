import { createRouter, createWebHistory } from "vue-router"
import HomePage from "../pages/HomePage.vue"
import LoginPage from "../pages/LoginPage.vue"
import NotFoundPage from "../pages/NotFoundPage.vue"
import PostPage from "../pages/PostPage.vue"
import ProjectPostsPage from "../pages/ProjectPostsPage.vue"
import ProjectsPage from "../pages/ProjectsPage.vue"
import RandomPostPage from "../pages/RandomPostPage.vue"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomePage,
    },
    {
      path: "/archive/",
      name: "projects",
      component: ProjectsPage,
    },
    {
      path: "/archive/random/",
      name: "random-post",
      component: RandomPostPage,
    },
    {
      path: "/archive/:project/",
      name: "project-posts",
      component: ProjectPostsPage,
    },
    {
      path: "/archive/:project/:postNumber/",
      name: "post",
      component: PostPage,
    },
    {
      path: "/login/",
      name: "login",
      component: LoginPage,
    },
    {
      path: "/projects/",
      redirect: "/archive/",
    },
    {
      path: "/projects/:project/",
      redirect: (to) => ({
        path: `/archive/${to.params.project}/`,
        query: to.query,
      }),
    },
    {
      path: "/projects/:project/:postNumber/",
      redirect: (to) => ({
        path: `/archive/${to.params.project}/${to.params.postNumber}/`,
        query: to.query,
      }),
    },
    {
      path: "/:pathMatch(.*)*",
      name: "not-found",
      component: NotFoundPage,
    },
  ],
})

export default router
