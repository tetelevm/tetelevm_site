<script setup>
import { formatDate } from "../../../utils/date.js"

defineProps({
  items: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <div class="post-card-list">
    <RouterLink
      v-for="item in items"
      :key="item.key"
      class="post-card"
      :to="item.link"
      :aria-label="item.alt || item.label"
    >
      <span class="post-card__image">
        <img
          v-if="item.image"
          :src="item.image"
          :alt="item.alt || item.label"
          loading="lazy"
        />
      </span>
      <span v-if="item.label || item.date" class="post-card__caption">
        <span
          v-if="item.label"
          class="post-card__label"
          :class="{ 'post-card__label--clamped': item.clampLabel }"
          :title="item.clampLabel ? item.label : undefined"
        >{{ item.label }}</span>
        <time
          v-if="item.date"
          class="post-card__date"
          :datetime="item.date"
        >{{ formatDate(item.date) }}</time>
        <span
          v-if="item.rating !== null && item.rating !== undefined"
          class="post-card__rating"
          aria-label="Оценка"
        >
          {{ item.rating }}
        </span>
      </span>
    </RouterLink>
  </div>
</template>

<style scoped>
.post-card-list {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: clamp(1rem, 2.5vw, 1.5rem);
}

.post-card {
  min-width: 0;
  display: flex;
  overflow: hidden;
  flex-direction: column;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-medium);
  color: var(--color-text);
  background: var(--color-surface);
  text-decoration: none;
  transition:
    transform 200ms ease,
    border-color 180ms ease,
    box-shadow 180ms ease;
}

.post-card__image {
  aspect-ratio: 1;
  display: block;
  overflow: hidden;
  background: var(--color-surface);
}

.post-card__image img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: center;
}

.post-card__caption {
  min-height: 3.75rem;
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: space-between;
  gap: 0.6rem;
  padding: 0.8rem;
}

.post-card__label {
  min-width: 0;
  overflow-wrap: anywhere;
  font-size: clamp(0.82rem, 2vw, 0.95rem);
  line-height: 1.3;
}

.post-card__label--clamped {
  display: -webkit-box;
  overflow: hidden;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  line-clamp: 3;
}

.post-card__rating {
  width: 2.15rem;
  height: 2.15rem;
  flex: 0 0 auto;
  display: grid;
  padding: 0.25rem;
  border: 1px solid rgba(215, 240, 111, 0.55);
  border-radius: 50%;
  color: var(--color-accent);
  background: var(--color-surface);
  font-size: 0.82rem;
  font-weight: 750;
  line-height: 1;
  font-family: var(--font-caption);
  place-items: center;
}

.post-card__date {
  flex: 0 0 auto;
  color: var(--color-text-muted);
  font-size: clamp(0.82rem, 2vw, 0.95rem);
  line-height: 1.3;
  font-family: var(--font-caption);
}

.post-card:hover,
.post-card:focus-visible {
  z-index: 2;
  border-color: rgba(215, 240, 111, 0.65);
  box-shadow: var(--shadow-card);
  outline: none;
  transform: translateY(-0.35rem);
}

.post-card:hover .post-card__label,
.post-card:focus-visible .post-card__label,
.post-card:hover .post-card__date,
.post-card:focus-visible .post-card__date,
.post-card:hover .post-card__rating,
.post-card:focus-visible .post-card__rating {
  color: var(--color-text);
}

.post-card:focus-visible {
  box-shadow: 0 0 0 3px var(--color-bg), 0 0 0 5px var(--color-accent);
}

@media (max-width: 640px) {
  .post-card-list {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 360px) {
  .post-card-list {
    grid-template-columns: 1fr;
  }
}

@media (prefers-reduced-motion: reduce) {
  .post-card,
  .post-card__image img {
    transition: none;
  }
}
</style>
