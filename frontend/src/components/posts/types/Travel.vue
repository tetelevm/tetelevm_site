<script setup>
import { computed } from "vue"

import MediaCarousel from "../../media/MediaCarousel.vue"
import MarkdownContent from "../blocks/MarkdownContent.vue"
import PlainPostText from "../blocks/PlainPostText.vue"
import PostLayout from "../blocks/PostLayout.vue"

const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
})

const photos = computed(() => {
  return (props.post.files ?? []).filter((item) => item.mediaType === "photo")
})
</script>

<template>
  <PostLayout :post="post">
    <MediaCarousel :items="photos" :label="`Фотографии: ${post.name}`" />

    <MarkdownContent v-if="post.extra?.md === true" :source="post.text" />
    <PlainPostText v-else :text="post.text" />

  </PostLayout>
</template>
