<script setup>
import { computed, ref, watch } from "vue"
import { useRoute } from "vue-router"

import { getPost } from "../api/projects.js"
import PageStatus from "../components/common/PageStatus.vue"
import PageSubheader from "../components/common/PageSubheader.vue"
import MainLayout from "../components/layout/MainLayout.vue"
import PostFooter from "../components/posts/blocks/PostFooter.vue"
import ProjectHeaderAction from "../components/projects/ProjectHeaderAction.vue"
import NotFoundPage from "./NotFoundPage.vue"
import {
  fileCountDescription,
  setPageMeta,
  textDescription,
} from "../utils/pageMeta.js"
import {
  DEFAULT_POST_COMPONENT,
  POST_COMPONENTS,
} from "../config/postTypes.js"

const route = useRoute()
const post = ref(null)
const isLoading = ref(false)
const errorMessage = ref("")
const isNotFound = ref(false)

const postComponent = computed(
  () => POST_COMPONENTS[post.value?.postType] ?? DEFAULT_POST_COMPONENT,
)

async function loadPost(projectCode, postNumber) {
  isLoading.value = true
  errorMessage.value = ""
  isNotFound.value = false
  post.value = null

  try {
    post.value = await getPost(projectCode, postNumber)
    const postName = post.value.name?.trim()
    const shortName = postName || `#${post.value.number}`
    setPageMeta({
      title: postName
        ? postName
        : `${post.value.projectName} #${post.value.number}`,
      socialTitle: `tetelevm - ${post.value.projectName} - ${shortName}`,
      description:
        textDescription(post.value.text) || fileCountDescription(post.value),
      image:
        post.value.mainFile?.mediaType === "photo"
          ? post.value.mainFile.link
          : "/favicon.ico",
      path: post.value.link,
      type: "article",
    })
  } catch (error) {
    isNotFound.value = error.status === 404
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
  <NotFoundPage v-if="isNotFound" />
  <MainLayout v-else active-page="formats">
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
        back-label="← к формату"
      />
    </template>

    <PageStatus
      v-if="isLoading || errorMessage"
      :loading="isLoading"
      :error="errorMessage"
    />
    <div v-else-if="post" class="post-page__content">
      <component :is="postComponent" :post="post" />
      <PostFooter
        :project-code="post.projectCode"
        :project-name="post.projectName"
        :related-posts="post.relatedPosts"
        :tags="post.tags"
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
