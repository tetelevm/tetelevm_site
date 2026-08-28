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
  <div class="post-row-list">
    <RouterLink
      v-for="item in items"
      :key="item.key"
      class="post-row"
      :to="item.link"
    >
      <span class="post-row__image">
        <img
          v-if="item.image"
          :src="item.image"
          :alt="item.alt || item.label"
          loading="lazy"
        />
      </span>
      <span class="post-row__content">
        <span class="post-row__top-line">
          <span class="post-row__label">{{ item.label }}</span>
          <span
            v-if="item.rating !== null && item.rating !== undefined"
            class="post-row__rating"
            aria-label="Оценка"
          >{{ item.rating }}</span>
        </span>
        <time
          v-if="item.date"
          class="post-row__date"
          :datetime="item.date"
        >{{ formatDate(item.date) }}</time>
      </span>
    </RouterLink>
  </div>
</template>

<style scoped>
.post-row-list {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.post-row {
  min-width: 0;
  min-height: 100px;
  display: grid;
  grid-template-columns: 100px minmax(0, 1fr);
  align-items: center;
  gap: 1rem;
  overflow: hidden;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-small);
  color: var(--color-text);
  background: var(--color-surface);
  text-decoration: none;
  transition:
    border-color 160ms ease,
    background-color 160ms ease,
    transform 180ms ease;
}

.post-row__image {
  width: 100px;
  height: 100px;
  align-self: stretch;
  display: block;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.12);
}

.post-row__image img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}

.post-row__content {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  padding-block: 1rem 0.5rem;
  padding-right: 1.15rem;
}

.post-row__top-line {
  min-width: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.post-row__label {
  min-width: 0;
  overflow-wrap: anywhere;
  font-size: clamp(1rem, 2.5vw, 1.2rem);
}

.post-row__rating {
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
  font-family: var(--font-caption);
  line-height: 1;
  place-items: center;
}

.post-row__date {
  color: var(--color-muted);
  font-size: 0.78rem;
  font-variant-numeric: tabular-nums;
  font-family: var(--font-caption);
  align-self: end;
}

.post-row:hover,
.post-row:focus-visible {
  border-color: rgba(215, 240, 111, 0.55);
  background: var(--color-surface-raised);
  outline: none;
  transform: translateX(0.2rem);
}

.post-row:hover .post-row__rating,
.post-row:focus-visible .post-row__rating {
  color: var(--color-text);
}

@media (max-width: 480px) {
  .post-row__content {
    padding-right: 0.75rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .post-row {
    transition: none;
  }
}
</style>
