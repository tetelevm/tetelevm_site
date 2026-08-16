<script setup>
defineProps({
  posts: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <div class="rated-post-grid">
    <RouterLink
      v-for="post in posts"
      :key="post.id ?? post.number"
      class="rated-post-card"
      :to="post.link"
    >
      <span class="rated-post-card__image">
        <img
          v-if="post.mainFile?.link"
          :src="post.mainFile.link"
          :alt="post.name"
          loading="lazy"
        />
      </span>
      <span class="rated-post-card__caption">
        <span class="rated-post-card__name">{{ post.name }}</span>
        <span
          v-if="post.rating !== null && post.rating !== undefined"
          class="rated-post-card__rating"
          aria-label="Оценка"
        >
          {{ post.rating }}
        </span>
      </span>
    </RouterLink>
  </div>
</template>

<style scoped>
.rated-post-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1.75rem 1rem;
}

.rated-post-card {
  min-width: 0;
  color: var(--color-text);
  text-decoration: none;
}

.rated-post-card__image {
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

.rated-post-card__image img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: center;
}

.rated-post-card__caption {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 0.6rem;
  margin-top: 0.55rem;
}

.rated-post-card__name {
  min-width: 0;
  overflow-wrap: anywhere;
  color: var(--color-muted);
  font-size: 0.82rem;
  line-height: 1.35;
}

.rated-post-card__rating {
  flex: 0 0 auto;
  color: var(--color-accent);
  font-size: 0.82rem;
  font-weight: 750;
  line-height: 1.35;
}

.rated-post-card:hover .rated-post-card__image,
.rated-post-card:focus-visible .rated-post-card__image {
  border-color: rgba(215, 240, 111, 0.65);
  box-shadow: var(--shadow-card);
  transform: translateY(-0.2rem);
}

.rated-post-card:hover .rated-post-card__name,
.rated-post-card:focus-visible .rated-post-card__name,
.rated-post-card:hover .rated-post-card__rating,
.rated-post-card:focus-visible .rated-post-card__rating {
  color: var(--color-text);
}

.rated-post-card:focus-visible {
  outline: none;
}

@media (max-width: 640px) {
  .rated-post-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 360px) {
  .rated-post-grid {
    grid-template-columns: 1fr;
  }
}

@media (prefers-reduced-motion: reduce) {
  .rated-post-card__image {
    transition: none;
  }
}
</style>
