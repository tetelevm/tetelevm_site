<script setup>
defineProps({
  posts: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <div class="photo-list">
    <RouterLink
      v-for="post in posts"
      :key="post.id ?? post.number"
      class="photo-card"
      :to="post.link"
      :aria-label="post.name || post.text || `Фотография ${post.number}`"
    >
      <img
        v-if="post.mainFile?.link"
        :src="post.mainFile.link"
        :alt="post.name || post.text"
        loading="lazy"
      />
    </RouterLink>
  </div>
</template>

<style scoped>
.photo-list {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.75rem;
}

.photo-card {
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

.photo-card img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: center;
}

.photo-card:hover,
.photo-card:focus-visible {
  border-color: rgba(215, 240, 111, 0.65);
  box-shadow: var(--shadow-card);
  outline: none;
  transform: translateY(-0.2rem);
}

@media (max-width: 640px) {
  .photo-list {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 360px) {
  .photo-list {
    grid-template-columns: 1fr;
  }
}

@media (prefers-reduced-motion: reduce) {
  .photo-card {
    transition: none;
  }
}
</style>
