<script setup>
import { computed } from "vue"

import LightboxImage from "../../media/LightboxImage.vue"
import PlainPostText from "../blocks/PlainPostText.vue"
import PostLayout from "../blocks/PostLayout.vue"
import RatedPostHeader from "../blocks/RatedPostHeader.vue"

const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
})

const screenshots = computed(() =>
  Array.from({ length: 3 }, (_, index) => props.post.files?.[index] ?? null),
)
</script>

<template>
  <PostLayout spacing="loose">
    <RatedPostHeader
      :title="post.name"
      :subtitle="post.extra?.original_title"
      :rating="post.extra?.rating"
      title-size="compact"
    />

    <div class="anime-post__screenshots" aria-label="Скриншоты">
      <div
        v-for="(file, index) in screenshots"
        :key="file?.id ?? `empty-${index}`"
        class="anime-post__screenshot"
      >
        <LightboxImage
          v-if="file?.link"
          :preview-src="file.link"
          :full-src="file.linkFull"
          :alt="`${post.name} — скриншот ${index + 1}`"
        />
        <span v-else>нет скриншота</span>
      </div>
    </div>

    <PlainPostText :text="post.text" />

    <p v-if="post.extra?.result" class="anime-post__result">
      <span>стоит смотреть:</span>
      <em>{{ post.extra.result }}</em>
    </p>
  </PostLayout>
</template>

<style scoped>
.anime-post__screenshots {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: clamp(0.5rem, 2vw, 1rem);
}

.anime-post__screenshot {
  aspect-ratio: 1;
  display: grid;
  overflow: hidden;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-small);
  color: var(--color-muted);
  background: var(--color-surface);
  font-size: 0.7rem;
  place-items: center;
  text-align: center;
}

.anime-post__result {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 0.35rem 0.65rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-line);
  margin: -1rem 0 0;
  color: var(--color-text);
  font-size: 1.2rem;
  line-height: 1.5;
}

.anime-post__result span {
  color: var(--color-accent);
  font-size: 0.9em;
  font-weight: 750;
  letter-spacing: 0.09em;
  text-transform: uppercase;
}

.anime-post__result em {
  color: var(--color-muted);
}

</style>
