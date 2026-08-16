<script setup>
import { onMounted, ref } from "vue"

import { getProjects } from "../api/projects.js"
import MainLayout from "../components/MainLayout.vue"
import ProjectGrid from "../components/ProjectGrid.vue"

const projects = ref([])
const isLoading = ref(false)
const errorMessage = ref("")

async function loadProjects() {
  isLoading.value = true
  errorMessage.value = ""

  try {
    const response = await getProjects()
    projects.value = response.map((project) => ({
      id: project.id,
      title: project.name,
      href: `/projects/${project.link}/`,
      image: project.cover,
      isPrivate: !project.isPublic,
    }))
  } catch (error) {
    errorMessage.value = error.message || "Не удалось загрузить проекты"
  } finally {
    isLoading.value = false
  }
}

onMounted(loadProjects)
</script>

<template>
  <MainLayout active-page="projects">
    <div class="projects-page__content">
      <h1 class="visually-hidden">Проекты</h1>
      <p v-if="isLoading" class="projects-page__status">Загрузка…</p>
      <p v-else-if="errorMessage" class="projects-page__status" role="alert">
        {{ errorMessage }}
      </p>
      <ProjectGrid v-else :projects="projects" />
    </div>
  </MainLayout>
</template>

<style scoped>
.projects-page__content {
  width: 100%;
}

.projects-page__status {
  margin: 0;
  color: var(--color-muted);
  text-align: center;
}
</style>
