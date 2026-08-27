<script setup>
import { computed, ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"

import { getProjectPosts } from "../api/projects.js"
import PageStatus from "../components/common/PageStatus.vue"
import PageSubheader from "../components/common/PageSubheader.vue"
import PaginationNav from "../components/common/PaginationNav.vue"
import MainLayout from "../components/layout/MainLayout.vue"
import NotFoundPage from "./NotFoundPage.vue"
import ProjectHeaderAction from "../components/projects/ProjectHeaderAction.vue"
import PostTag from "../components/posts/blocks/PostTag.vue"
import { setPageMeta, textDescription } from "../utils/pageMeta.js"
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
const isNotFound = ref(false)

const postListComponent = computed(
  () =>
    POST_LIST_COMPONENTS[project.value?.postListType] ??
    DEFAULT_POST_LIST_COMPONENT,
)

function routePage() {
  const page = Number.parseInt(route.query.page, 10)
  return Number.isInteger(page) && page > 0 ? page : 1
}

function routeTag() {
  return typeof route.query.tag === "string" ? route.query.tag.trim() : ""
}

async function loadProject(link, page, tagCode) {
  isLoading.value = true
  errorMessage.value = ""
  isNotFound.value = false
  project.value = null
  pagination.value = null

  try {
    const response = await getProjectPosts(link, page, tagCode)
    project.value = response
    pagination.value = response.pagination
    setPageMeta({
      title: response.name,
      socialTitle: `tetelevm - ${response.name}`,
      description: textDescription(response.description),
      image: response.cover,
      path: `/archive/${response.link}/`,
    })
  } catch (error) {
    isNotFound.value = error.status === 404
    errorMessage.value = error.message || "Не удалось загрузить формат"
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
  () => [route.params.project, route.query.page, route.query.tag],
  ([link]) => loadProject(link, routePage(), routeTag()),
  { immediate: true },
)
</script>

<template>
  <NotFoundPage v-if="isNotFound" />
  <MainLayout v-else active-page="formats">
    <template #header-action>
      <ProjectHeaderAction
        v-if="project"
        :project-name="project.name"
      />
    </template>

    <template #subheader>
      <PageSubheader
        back-to="/archive/"
        back-label="← форматы"
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
      <ul
        v-if="project.activeTag"
        class="project-posts__active-tag"
        aria-label="Выбранный тег"
      >
        <PostTag
          :code="project.activeTag.code"
          :name="project.activeTag.name"
          :project-code="project.link"
          :linked="false"
        />
      </ul>
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

<style scoped>
.project-posts__active-tag {
  display: flex;
  flex-wrap: wrap;
  padding: 0;
  margin: 0 0 1.25rem;
  list-style: none;
}
</style>
