<script setup>
import { computed, ref, watch } from "vue"
import { useRoute } from "vue-router"

import { getPost } from "../api/projects.js"
import LoginLink from "../components/LoginLink.vue"
import MainLayout from "../components/MainLayout.vue"
import AbandonedPost from "../components/post-types/Abandoned.vue"
import DoorPost from "../components/post-types/Door.vue"
import PhotoPost from "../components/post-types/Photo.vue"
import PlasticinePost from "../components/post-types/Plasticine.vue"
import Post from "../components/post-types/Post.vue"
import ReviewPost from "../components/post-types/Review.vue"
import TextPost from "../components/post-types/Text.vue"
import TextMdPost from "../components/post-types/TextMd.vue"
import TravelPost from "../components/post-types/Travel.vue"

const POST_COMPONENTS = {
  post: Post,
  photo: PhotoPost,
  travel: TravelPost,
  text: TextPost,
  text_md: TextMdPost,
  door: DoorPost,
  review: ReviewPost,
  plasticine: PlasticinePost,
  abandoned: AbandonedPost,
}

const route = useRoute()
const post = ref(null)
const isLoading = ref(false)
const errorMessage = ref("")

const postComponent = computed(
  () => POST_COMPONENTS[post.value?.postType] ?? Post,
)

async function loadPost(projectCode, postNumber) {
  isLoading.value = true
  errorMessage.value = ""
  post.value = null

  try {
    post.value = await getPost(projectCode, postNumber)
  } catch (error) {
    errorMessage.value = error.message || "Не удалось загрузить пост"
  } finally {
    isLoading.value = false
  }
}

watch(
  () => [route.params.project, route.params.postNumber],
  ([projectCode, postNumber]) => loadPost(projectCode, postNumber),
  { immediate: true },
)
</script>

<template>
  <MainLayout active-page="projects">
    <template #header-action>
      <LoginLink />
    </template>

    <p v-if="isLoading" class="post-page__status">Загрузка…</p>
    <p v-else-if="errorMessage" class="post-page__status" role="alert">
      {{ errorMessage }}
    </p>
    <template v-else-if="post">
      <h1 class="visually-hidden">{{ post.name || post.text }}</h1>
      <component :is="postComponent" :post="post" />
    </template>
  </MainLayout>
</template>

<style scoped>
.post-page__status {
  margin: 0;
  color: rgba(255, 255, 255, 0.72);
  text-align: center;
}
</style>
