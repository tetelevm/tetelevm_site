<script setup>
import { computed } from "vue"

import DatedPostHeader from "../DatedPostHeader.vue"
import MediaCarousel from "../MediaCarousel.vue"

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
  <article class="text-post">
    <DatedPostHeader :title="post.name" :date="post.date" />

    <div class="text-post__body">{{ post.text }}</div>

    <MediaCarousel :items="mediaItems" :label="`Медиа: ${post.name}`" />
  </article>
</template>

<style scoped>
.text-post {
  display: flex;
  flex-direction: column;
  gap: clamp(1.75rem, 4vw, 2.75rem);
}

.text-post__body {
  color: var(--color-text);
  font-size: 1.2rem;
  line-height: 1.65;
  white-space: pre-line;
}

</style>
