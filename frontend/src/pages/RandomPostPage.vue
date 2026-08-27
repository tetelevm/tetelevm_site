<script setup>
import { onMounted, ref } from "vue"
import { useRouter } from "vue-router"

import { getRandomPost } from "../api/projects.js"
import PageStatus from "../components/common/PageStatus.vue"
import MainLayout from "../components/layout/MainLayout.vue"

const router = useRouter()
const errorMessage = ref("")

async function openRandomPost() {
  try {
    const post = await getRandomPost()
    await router.replace(post.link)
  } catch (error) {
    errorMessage.value = error.message || "Не удалось выбрать случайный пост"
  }
}

onMounted(openRandomPost)
</script>

<template>
  <MainLayout active-page="formats">
    <PageStatus
      :loading="!errorMessage"
      :error="errorMessage"
      loading-text="Выбираем случайный пост…"
    />
  </MainLayout>
</template>
