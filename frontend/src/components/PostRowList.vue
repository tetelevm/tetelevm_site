<script setup>
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
      <span class="post-row__label">{{ item.label }}</span>
      <span v-if="item.date" class="post-row__date">{{ item.date }}</span>
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
  grid-template-columns: 100px minmax(0, 1fr) auto;
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

.post-row__label {
  min-width: 0;
  padding-block: 1rem;
  overflow-wrap: anywhere;
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(1rem, 2.5vw, 1.2rem);
}

.post-row__date {
  flex: 0 0 auto;
  padding: 1rem 1.15rem 1rem 0;
  color: var(--color-muted);
  font-size: 0.78rem;
  font-variant-numeric: tabular-nums;
}

.post-row:hover,
.post-row:focus-visible {
  border-color: rgba(215, 240, 111, 0.55);
  background: var(--color-surface-raised);
  outline: none;
  transform: translateX(0.2rem);
}

@media (max-width: 480px) {
  .post-row {
    grid-template-columns: 100px minmax(0, 1fr);
    align-items: start;
  }

  .post-row__label {
    padding-right: 0.75rem;
  }

  .post-row__date {
    grid-column: 2;
    padding: 0 0.75rem 0.75rem 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .post-row {
    transition: none;
  }
}
</style>
