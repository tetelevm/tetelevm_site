<script setup>
import { computed } from "vue"

import MediaCarousel from "../../media/MediaCarousel.vue"
import DatedPostHeader from "../blocks/DatedPostHeader.vue"
import PlainPostText from "../blocks/PlainPostText.vue"
import PostConnections from "../blocks/PostConnections.vue"
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
  <PostLayout>
    <DatedPostHeader :title="post.name" :date="post.date" />

    <MediaCarousel :items="photos" :label="`Фотографии: ${post.name}`" />

    <PlainPostText :text="post.text" />

    <PostConnections
      :related-posts="post.relatedPosts"
      :tags="post.tags"
    />
  </PostLayout>
</template>
