<script setup>
import { computed, ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"

import { getProjectPosts } from "../api/projects.js"
import LoginLink from "../components/LoginLink.vue"
import MainLayout from "../components/MainLayout.vue"
import ProjectHeaderAction from "../components/ProjectHeaderAction.vue"
import AbandonedList from "../components/post-list-types/Abandoned.vue"
import DoorList from "../components/post-list-types/Door.vue"
import PhotoList from "../components/post-list-types/Photo.vue"
import PlasticineList from "../components/post-list-types/Plasticine.vue"
import PostList from "../components/post-list-types/Post.vue"
import ReviewList from "../components/post-list-types/Review.vue"
import TextList from "../components/post-list-types/Text.vue"
import TextMdList from "../components/post-list-types/TextMd.vue"
import TravelList from "../components/post-list-types/Travel.vue"

const POST_LIST_COMPONENTS = {
  post: PostList,
  photo: PhotoList,
  travel: TravelList,
  text: TextList,
  text_md: TextMdList,
  door: DoorList,
  review: ReviewList,
  plasticine: PlasticineList,
  abandoned: AbandonedList,
}

const route = useRoute()
const router = useRouter()
const project = ref(null)
const pagination = ref(null)
const isLoading = ref(false)
const errorMessage = ref("")

const postListComponent = computed(
  () => POST_LIST_COMPONENTS[project.value?.postListType] ?? PostList,
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
      <LoginLink v-else />
    </template>

    <template #subheader>
      <div class="project-posts-page__toolbar">
        <RouterLink to="/projects/">← все проекты</RouterLink>
        <span v-if="pagination">материалов: {{ pagination.totalItems }}</span>
      </div>
    </template>

    <p v-if="isLoading" class="project-posts-page__status">Загрузка…</p>
    <p v-else-if="errorMessage" class="project-posts-page__status" role="alert">
      {{ errorMessage }}
    </p>
    <template v-else-if="project">
      <h1 class="visually-hidden">{{ project.name }}</h1>
      <component
        :is="postListComponent"
        :posts="project.posts"
      />
      <nav
        v-if="pagination.totalPages > 1"
        class="project-posts-page__pagination"
        aria-label="Страницы постов"
      >
        <button
          v-for="page in pagination.totalPages"
          :key="page"
          class="project-posts-page__page"
          :class="{ 'project-posts-page__page--active': page === pagination.page }"
          type="button"
          :aria-current="page === pagination.page ? 'page' : undefined"
          @click="switchPage(page)"
        >
          {{ page }}
        </button>
      </nav>
    </template>
  </MainLayout>
</template>

<style scoped>
.project-posts-page__status {
  margin: 0;
  color: var(--color-muted);
  text-align: center;
}

.project-posts-page__toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.project-posts-page__toolbar a,
.project-posts-page__toolbar span {
  color: var(--color-muted);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-decoration: none;
  text-transform: uppercase;
}

.project-posts-page__toolbar a:hover,
.project-posts-page__toolbar a:focus-visible {
  color: var(--color-accent);
  outline: none;
}

.project-posts-page__pagination {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.4rem;
  margin-top: 3.5rem;
}

.project-posts-page__page {
  min-width: 2.4rem;
  padding: 0.5rem 0.65rem;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-small);
  color: var(--color-muted);
  background: var(--color-surface);
  cursor: pointer;
}

.project-posts-page__page:hover,
.project-posts-page__page:focus-visible,
.project-posts-page__page--active {
  border-color: rgba(215, 240, 111, 0.6);
  color: var(--color-text);
  outline: none;
}

.project-posts-page__page--active {
  border-color: var(--color-accent);
  color: #151612;
  background: var(--color-accent);
}
</style>
