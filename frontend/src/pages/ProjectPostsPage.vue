<script setup>
import { computed, ref, watch } from "vue"
import { useRoute } from "vue-router"

import { getProject } from "../api/projects.js"
import LoginLink from "../components/LoginLink.vue"
import MainLayout from "../components/MainLayout.vue"
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
const project = ref(null)
const isLoading = ref(false)
const errorMessage = ref("")

const postListComponent = computed(
  () => POST_LIST_COMPONENTS[project.value?.postListType] ?? PostList,
)

async function loadProject(link) {
  isLoading.value = true
  errorMessage.value = ""
  project.value = null

  try {
    project.value = await getProject(link)
  } catch (error) {
    errorMessage.value = error.message || "Не удалось загрузить проект"
  } finally {
    isLoading.value = false
  }
}

watch(
  () => route.params.project,
  (link) => loadProject(link),
  { immediate: true },
)
</script>

<template>
  <MainLayout active-page="projects">
    <template #header-action>
      <LoginLink />
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
    </template>
  </MainLayout>
</template>

<style scoped>
.project-posts-page__status {
  margin: 0;
  color: rgba(255, 255, 255, 0.72);
  text-align: center;
}
</style>
