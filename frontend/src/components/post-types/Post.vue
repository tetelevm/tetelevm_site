<script setup>
import { computed } from "vue"

import DatedPostHeader from "../DatedPostHeader.vue"
import LightboxImage from "../LightboxImage.vue"
import MediaCarousel from "../MediaCarousel.vue"
import PostFileList from "../PostFileList.vue"
import PostTag from "../PostTag.vue"
import RelatedPostLink from "../RelatedPostLink.vue"

const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
})

const mediaFiles = computed(() =>
  (props.post.files ?? []).filter((file) =>
    ["photo", "video"].includes(file.mediaType),
  ),
)

const otherFiles = computed(() =>
  (props.post.files ?? []).filter(
    (file) => !["photo", "video"].includes(file.mediaType),
  ),
)
</script>

<template>
  <article class="post-post">
    <DatedPostHeader :title="post.name" :date="post.date" />

    <div v-if="post.text" class="post-post__text">{{ post.text }}</div>

    <div v-if="post.mainFile?.mediaType === 'photo'" class="post-post__main-image">
      <LightboxImage
        :preview-src="post.mainFile.link"
        :full-src="post.mainFile.linkFull"
        :alt="post.name"
        preview-fit="contain"
      />
    </div>

    <MediaCarousel :items="mediaFiles" :label="`Медиа: ${post.name}`" />

    <PostFileList :files="otherFiles" />

    <RelatedPostLink
      v-if="post.relatedPost"
      :related-post="post.relatedPost"
    />

    <ul v-if="post.tags?.length" class="post-post__tags" aria-label="Теги">
      <PostTag
        v-for="tag in post.tags"
        :key="tag.code"
        :name="tag.name"
      />
    </ul>
  </article>
</template>

<style scoped>
.post-post {
  display: flex;
  flex-direction: column;
  gap: clamp(1.75rem, 4vw, 2.75rem);
}

.post-post__main-image {
  width: 100%;
  aspect-ratio: 16 / 10;
  overflow: hidden;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-medium);
  background: #0d0e0c;
  box-shadow: var(--shadow-card);
}

.post-post__text {
  color: var(--color-text);
  font-size: 1.2rem;
  line-height: 1.65;
  white-space: pre-line;
}

.post-post__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding: 0;
  margin: -0.5rem 0 0;
  list-style: none;
}

@media (max-width: 480px) {
  .post-post__main-image {
    aspect-ratio: 1;
  }
}
</style>
