<script setup>
import { computed } from "vue"

import MediaCarousel from "../../media/MediaCarousel.vue"
import PlainPostText from "../blocks/PlainPostText.vue"
import PostLayout from "../blocks/PostLayout.vue"

const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
})

const mediaItems = computed(() => {
  const items = [props.post.mainFile, ...(props.post.files ?? [])].filter(Boolean)
  return items.filter(
    (item, index) =>
      items.findIndex((candidate) => candidate.id === item.id) === index,
  )
})
</script>

<template>
  <PostLayout :post="post">
    <PlainPostText :text="post.text" />

    <MediaCarousel :items="mediaItems" :label="`Медиа: ${post.name}`" />
  </PostLayout>
</template>
