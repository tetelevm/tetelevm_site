<script setup>
import { computed, ref, watch } from "vue"
import { useRoute } from "vue-router"

import { getPost } from "../api/projects.js"
import PageStatus from "../components/common/PageStatus.vue"
import PageSubheader from "../components/common/PageSubheader.vue"
import MainLayout from "../components/layout/MainLayout.vue"
import PostNavigation from "../components/posts/blocks/PostNavigation.vue"
import ProjectHeaderAction from "../components/projects/ProjectHeaderAction.vue"
import {
  DEFAULT_POST_COMPONENT,
  POST_COMPONENTS,
} from "../config/postTypes.js"

const route = useRoute()
const post = ref(null)
const isLoading = ref(false)
const errorMessage = ref("")

const postComponent = computed(
  () => POST_COMPONENTS[post.value?.postType] ?? DEFAULT_POST_COMPONENT,
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
      <ProjectHeaderAction
        v-if="post"
        :project-name="post.projectName"
      />
    </template>

    <template #subheader>
      <PageSubheader
        v-if="post"
        :back-to="`/archive/${post.projectCode}/`"
        back-label="← к проекту"
      />
    </template>

    <PageStatus
      v-if="isLoading || errorMessage"
      :loading="isLoading"
      :error="errorMessage"
    />
    <div v-else-if="post" class="post-page__content">
      <component :is="postComponent" :post="post" />
      <PostNavigation
        :project-name="post.projectName"
        :previous-post="post.previousPost"
        :next-post="post.nextPost"
      />
    </div>
  </MainLayout>
</template>

<style scoped>
.post-page__content {
  display: flex;
  flex-direction: column;
  gap: clamp(2.5rem, 6vw, 4.5rem);
}
</style>
