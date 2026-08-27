<script setup>
import { onMounted, ref } from "vue"

import { getProjects } from "../api/projects.js"
import PageStatus from "../components/common/PageStatus.vue"
import MainLayout from "../components/layout/MainLayout.vue"
import ProjectGrid from "../components/projects/ProjectGrid.vue"

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
      href: `/archive/${project.link}/`,
      image: project.cover,
      isPrivate: !project.isPublic,
      status: project.status,
      postCount: project.postCount,
    }))
  } catch (error) {
    errorMessage.value = error.message || "Не удалось загрузить архив"
  } finally {
    isLoading.value = false
  }
}

onMounted(loadProjects)
</script>

<template>
  <MainLayout active-page="formats">
    <h1 class="visually-hidden">Форматы</h1>
    <PageStatus
      v-if="isLoading || errorMessage"
      :loading="isLoading"
      :error="errorMessage"
    />
    <ProjectGrid v-else :projects="projects" />
  </MainLayout>
</template>
