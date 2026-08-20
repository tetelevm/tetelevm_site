<script setup>
import { computed, ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"

import { getProjectPosts } from "../api/projects.js"
import PageStatus from "../components/common/PageStatus.vue"
import PageSubheader from "../components/common/PageSubheader.vue"
import PaginationNav from "../components/common/PaginationNav.vue"
import MainLayout from "../components/layout/MainLayout.vue"
import ProjectHeaderAction from "../components/projects/ProjectHeaderAction.vue"
import {
  DEFAULT_POST_LIST_COMPONENT,
  POST_LIST_COMPONENTS,
} from "../config/postTypes.js"

const route = useRoute()
const router = useRouter()
const project = ref(null)
const pagination = ref(null)
const isLoading = ref(false)
const errorMessage = ref("")

const postListComponent = computed(
  () =>
    POST_LIST_COMPONENTS[project.value?.postListType] ??
    DEFAULT_POST_LIST_COMPONENT,
)

function routePage() {
  const page = Number.parseInt(route.query.page, 10)
  return Number.isInteger(page) && page > 0 ? page : 1
}

async function loadProject(link, page) {
  isLoading.value = true
  errorMessage.value = ""
  project.value = null
  pagination.value = null

  try {
    const response = await getProjectPosts(link, page)
    project.value = response
    pagination.value = response.pagination
  } catch (error) {
    errorMessage.value = error.message || "Не удалось загрузить проект"
  } finally {
    isLoading.value = false
  }
}

function switchPage(page) {
  if (page === pagination.value?.page) {
    return
  }
  router.push({
    query: {
      ...route.query,
      page: page === 1 ? undefined : String(page),
    },
  })
}

watch(
  () => [route.params.project, route.query.page],
  ([link]) => loadProject(link, routePage()),
  { immediate: true },
)
</script>

<template>
  <MainLayout active-page="projects">
    <template #header-action>
      <ProjectHeaderAction
        v-if="project"
        :project-name="project.name"
      />
    </template>

    <template #subheader>
      <PageSubheader
        back-to="/projects/"
        back-label="← все проекты"
        :meta="pagination ? `материалов: ${pagination.totalItems}` : ''"
        :status="project?.status"
        :description="project?.description"
      />
    </template>

    <PageStatus
      v-if="isLoading || errorMessage"
      :loading="isLoading"
      :error="errorMessage"
    />
    <template v-else-if="project">
      <h1 class="visually-hidden">{{ project.name }}</h1>
      <component
        :is="postListComponent"
        :posts="project.posts"
      />
      <PaginationNav
        :current-page="pagination.page"
        :total-pages="pagination.totalPages"
        label="Страницы постов"
        @select="switchPage"
      />
    </template>
  </MainLayout>
</template>
