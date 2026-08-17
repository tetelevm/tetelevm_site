<script setup>
defineProps({
  posts: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <div class="text-post-list">
    <RouterLink
      v-for="post in posts"
      :key="post.id ?? post.number"
      class="text-post-list__item"
      :to="post.link"
    >
      <span class="text-post-list__thumbnail">
        <img
          v-if="post.thumbnail || post.mainFile?.mediaType === 'photo'"
          :src="post.thumbnail || post.mainFile.link"
          :alt="post.label || post.name"
          loading="lazy"
        />
      </span>
      <span class="text-post-list__name">{{ post.label || post.name }}</span>
      <span v-if="post.date" class="text-post-list__date">{{ post.date }}</span>
    </RouterLink>
  </div>
</template>

<style scoped>
.text-post-list {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.text-post-list__item {
  min-width: 0;
  min-height: 150px;
  display: grid;
  grid-template-columns: 150px minmax(0, 1fr) auto;
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

.text-post-list__thumbnail {
  width: 150px;
  height: 150px;
  align-self: stretch;
  display: block;
  overflow: hidden;
  border-right: 1px solid var(--color-line);
  background: rgba(0, 0, 0, 0.12);
}

.text-post-list__thumbnail img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}

.text-post-list__name {
  min-width: 0;
  padding-block: 1rem;
  overflow-wrap: anywhere;
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(1rem, 2.5vw, 1.2rem);
}

.text-post-list__date {
  flex: 0 0 auto;
  padding: 1rem 1.15rem 1rem 0;
  color: var(--color-muted);
  font-size: 0.78rem;
  font-variant-numeric: tabular-nums;
}

.text-post-list__item:hover,
.text-post-list__item:focus-visible {
  border-color: rgba(215, 240, 111, 0.55);
  background: var(--color-surface-raised);
  outline: none;
  transform: translateX(0.2rem);
}

@media (max-width: 480px) {
  .text-post-list__item {
    grid-template-columns: 150px minmax(0, 1fr);
    align-items: start;
  }

  .text-post-list__name {
    padding-right: 0.75rem;
  }

  .text-post-list__date {
    grid-column: 2;
    padding: 0 0.75rem 0.75rem 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .text-post-list__item {
    transition: none;
  }
}
</style>
