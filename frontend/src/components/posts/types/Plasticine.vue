<script setup>
import { computed } from "vue"

import { formatDate } from "../../../utils/date.js"
import MediaCarousel from "../../media/MediaCarousel.vue"
import PostImage from "../blocks/PostImage.vue"
import PostLayout from "../blocks/PostLayout.vue"

const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
})

const additionalPhotos = computed(() =>
  (props.post.files ?? []).filter((file) => file.mediaType === "photo"),
)
</script>

<template>
  <PostLayout spacing="compact" align="center">
    <figure
      v-if="post.mainFile?.link"
      class="plasticine-post__main"
      :class="{
        'plasticine-post__main--with-gallery': additionalPhotos.length,
      }"
    >
      <PostImage
        :src="post.mainFile.linkFull || post.mainFile.link"
        :full-src="post.mainFile.linkFull"
        :alt="post.name || post.text"
        lightbox
      />
    </figure>

    <MediaCarousel
      class="plasticine-post__carousel"
      :items="additionalPhotos"
      label="Дополнительные фотографии"
    />

    <time
      v-if="post.date"
      class="plasticine-post__date"
      :datetime="post.date"
    >{{ formatDate(post.date) }}</time>
  </PostLayout>
</template>

<style scoped>
.plasticine-post__main {
  width: 100%;
  margin: 0;
}

.plasticine-post__main--with-gallery {
  padding-bottom: clamp(1rem, 2.5vw, 1.5rem);
  border-bottom: 1px solid var(--color-line);
}

.plasticine-post__carousel {
  width: 100%;
}

.plasticine-post__date {
  align-self: center;
  color: var(--color-muted);
  font-size: 1.25rem;
  font-variant-numeric: tabular-nums;
  text-align: center;
  margin-top: 1.5rem;
}
</style>
