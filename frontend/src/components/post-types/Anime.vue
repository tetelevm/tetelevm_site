<script setup>
import { computed } from "vue"

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
  <article class="anime-post">
    <header class="anime-post__header">
      <div class="anime-post__titles">
        <h1>{{ post.name }}</h1>
        <p v-if="post.extra?.original_title" class="anime-post__original-title">
          {{ post.extra.original_title }}
        </p>
      </div>
      <div
        v-if="post.extra?.rating !== undefined && post.extra?.rating !== null"
        class="anime-post__rating"
        aria-label="Оценка"
      >
        {{ post.extra.rating }}
      </div>
    </header>

    <div class="anime-post__screenshots" aria-label="Скриншоты">
      <div
        v-for="(file, index) in screenshots"
        :key="file?.id ?? `empty-${index}`"
        class="anime-post__screenshot"
      >
        <img
          v-if="file?.link"
          :src="file.link"
          :alt="`${post.name} — скриншот ${index + 1}`"
          loading="lazy"
        />
        <span v-else>нет скриншота</span>
      </div>
    </div>

    <div v-if="post.text" class="anime-post__text">{{ post.text }}</div>

    <p v-if="post.extra?.result" class="anime-post__result">
      <span>стоит смотреть:</span>
      <em>{{ post.extra.result }}</em>
    </p>
  </article>
</template>

<style scoped>
.anime-post {
  display: flex;
  flex-direction: column;
  gap: clamp(2rem, 5vw, 3.5rem);
}

.anime-post__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
}

.anime-post__titles {
  min-width: 0;
}

.anime-post__titles h1 {
  margin: 0;
  color: var(--color-text);
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(2rem, 6vw, 3.4rem);
  font-weight: 500;
  line-height: 1.05;
}

.anime-post__original-title {
  margin: 0.35rem 0 0;
  color: var(--color-muted);
  font-size: clamp(0.95rem, 2.5vw, 1.1rem);
  font-style: italic;
  line-height: 1.35;
}

.anime-post__rating {
  min-width: 3.8rem;
  min-height: 3.8rem;
  flex: 0 0 auto;
  display: grid;
  padding: 0.6rem;
  border: 1px solid rgba(215, 240, 111, 0.55);
  border-radius: 50%;
  color: var(--color-accent);
  background: var(--color-surface);
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.55rem;
  line-height: 1;
  place-items: center;
}

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

.anime-post__screenshot img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}

.anime-post__text {
  color: var(--color-text);
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(1rem, 2.4vw, 1.15rem);
  line-height: 1.75;
  white-space: pre-line;
}

.anime-post__result {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem 0.65rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-line);
  margin: -1rem 0 0;
  color: var(--color-text);
  line-height: 1.5;
}

.anime-post__result span {
  color: var(--color-accent);
  font-size: 0.75rem;
  font-weight: 750;
  letter-spacing: 0.09em;
  text-transform: uppercase;
}

.anime-post__result em {
  color: var(--color-muted);
}

@media (max-width: 480px) {
  .anime-post__header {
    align-items: flex-start;
  }

  .anime-post__rating {
    min-width: 3.2rem;
    min-height: 3.2rem;
    font-size: 1.25rem;
  }
}
</style>
