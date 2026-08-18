<script setup>
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
      <span v-if="item.label" class="post-card__caption">
        <span class="post-card__label">{{ item.label }}</span>
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
  gap: 1.75rem 1rem;
}

.post-card {
  min-width: 0;
  color: var(--color-text);
  text-decoration: none;
}

.post-card__image {
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

.post-card__image img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: center;
}

.post-card__caption {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 0.6rem;
  margin-top: 0.55rem;
}

.post-card__label {
  min-width: 0;
  overflow-wrap: anywhere;
  color: var(--color-muted);
  font-size: 0.82rem;
  line-height: 1.35;
}

.post-card__rating {
  flex: 0 0 auto;
  color: var(--color-accent);
  font-size: 0.82rem;
  font-weight: 750;
  line-height: 1.35;
}

.post-card:hover .post-card__image,
.post-card:focus-visible .post-card__image {
  border-color: rgba(215, 240, 111, 0.65);
  box-shadow: var(--shadow-card);
  transform: translateY(-0.2rem);
}

.post-card:hover .post-card__label,
.post-card:focus-visible .post-card__label,
.post-card:hover .post-card__rating,
.post-card:focus-visible .post-card__rating {
  color: var(--color-text);
}

.post-card:focus-visible {
  outline: none;
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
  .post-card__image {
    transition: none;
  }
}
</style>
