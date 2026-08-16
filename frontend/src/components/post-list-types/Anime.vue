<script setup>
defineProps({
  posts: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <div class="anime-list">
    <RouterLink
      v-for="post in posts"
      :key="post.id ?? post.number"
      class="anime-card"
      :to="post.link"
    >
      <span class="anime-card__image">
        <img
          v-if="post.mainFile?.link"
          :src="post.mainFile.link"
          :alt="post.name"
        />
      </span>
      <span class="anime-card__caption">
        <span class="anime-card__name">{{ post.name }}</span>
        <span
          v-if="post.rating !== null && post.rating !== undefined"
          class="anime-card__rating"
          aria-label="Оценка"
        >
          {{ post.rating }}
        </span>
      </span>
    </RouterLink>
  </div>
</template>

<style scoped>
.anime-list {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1.75rem 1rem;
}

.anime-card {
  min-width: 0;
  color: var(--color-text);
  text-decoration: none;
}

.anime-card__image {
  aspect-ratio: 1;
  display: block;
  overflow: hidden;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-small);
  background: var(--color-surface);
  transition:
    border-color 160ms ease,
    box-shadow 180ms ease,
    transform 180ms ease;
}

.anime-card__image img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: center;
}

.anime-card__caption {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 0.6rem;
  margin-top: 0.55rem;
}

.anime-card__name {
  min-width: 0;
  overflow-wrap: anywhere;
  color: var(--color-muted);
  font-size: 0.82rem;
  line-height: 1.35;
}

.anime-card__rating {
  flex: 0 0 auto;
  color: var(--color-accent);
  font-size: 0.82rem;
  font-weight: 750;
  line-height: 1.35;
}

.anime-card:hover .anime-card__image,
.anime-card:focus-visible .anime-card__image {
  border-color: rgba(215, 240, 111, 0.65);
  box-shadow: var(--shadow-card);
  transform: translateY(-0.2rem);
}

.anime-card:hover .anime-card__name,
.anime-card:focus-visible .anime-card__name,
.anime-card:hover .anime-card__rating,
.anime-card:focus-visible .anime-card__rating {
  color: var(--color-text);
}

.anime-card:focus-visible {
  outline: none;
}

@media (max-width: 640px) {
  .anime-list {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 360px) {
  .anime-list {
    grid-template-columns: 1fr;
  }
}

@media (prefers-reduced-motion: reduce) {
  .anime-card__image {
    transition: none;
  }
}
</style>
