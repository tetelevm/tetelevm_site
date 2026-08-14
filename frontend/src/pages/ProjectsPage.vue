<script setup>
import LoginLink from "../components/LoginLink.vue"
import MainLayout from "../components/MainLayout.vue"
import ProjectGrid from "../components/ProjectGrid.vue"

const projects = [
  {
    id: 1,
    title: "Проект 01",
    href: "/content/project-01/",
    image: "",
    accent: "#dbcc4f",
    isPrivate: false,
  },
  {
    id: 2,
    title: "Проект 02",
    href: "/content/project-02/",
    image: "",
    accent: "#a8bd78",
    isPrivate: false,
  },
  {
    id: 3,
    title: "Проект 03",
    href: "/content/project-03/",
    image: "",
    accent: "#cf9866",
    isPrivate: false,
  },
  {
    id: 4,
    title: "Проект 04",
    href: "/content/project-04/",
    image: "",
    accent: "#7ca1aa",
    isPrivate: false,
  },
  {
    id: 5,
    title: "Проект 05",
    href: "/content/project-05/",
    image: "",
    accent: "#a990bd",
    isPrivate: true,
  },
  {
    id: 6,
    title: "Проект 06",
    href: "/content/project-06/",
    image: "",
    accent: "#be7975",
    isPrivate: true,
  },
  {
    id: 7,
    title: "Проект 07",
    href: "/content/project-07/",
    image: "",
    accent: "#8f9f67",
    isPrivate: true,
  },
]
</script>

<template>
  <MainLayout active-page="projects">
    <template #header-action>
        <LoginLink />
    </template>

    <div class="projects-page__content">
      <h1 class="visually-hidden">Проекты</h1>
      <ProjectGrid :projects="projects" />
    </div>
  </MainLayout>
</template>

<style scoped>
.projects-page__content {
  width: 100%;
}
</style>
