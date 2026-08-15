<script setup>
defineProps({
  posts: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <div class="door-list">
    <RouterLink
      v-for="post in posts"
      :key="post.id ?? post.number"
      class="door-card"
      :to="post.link"
    >
      <span class="door-card__photo">
        <img
          v-if="post.mainFile?.link"
          :src="post.mainFile.link"
          :alt="post.text"
        />
      </span>
      <span class="door-card__caption">{{ post.text }}</span>
    </RouterLink>
  </div>
</template>

<style scoped>
.door-list {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1.75rem 1rem;
}

.door-card {
  min-width: 0;
  color: var(--color-text);
  text-decoration: none;
}

.door-card__photo {
  aspect-ratio: 1;
  display: block;
  overflow: hidden;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-small);
  background: var(--color-surface);
  transition:
    border-color 160ms ease,
    transform 180ms ease,
    box-shadow 180ms ease;
}

.door-card__photo img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: center;
}

.door-card__caption {
  display: block;
  margin-top: 0.55rem;
  overflow-wrap: anywhere;
  color: var(--color-muted);
  font-size: 0.82rem;
  line-height: 1.35;
}

.door-card:hover .door-card__photo,
.door-card:focus-visible .door-card__photo {
  border-color: rgba(215, 240, 111, 0.65);
  box-shadow: var(--shadow-card);
  transform: translateY(-0.2rem);
}

.door-card:hover .door-card__caption,
.door-card:focus-visible .door-card__caption {
  color: var(--color-text);
}

.door-card:focus-visible {
  outline: none;
}

@media (max-width: 640px) {
  .door-list {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 360px) {
  .door-list {
    grid-template-columns: 1fr;
  }
}

@media (prefers-reduced-motion: reduce) {
  .door-card__photo {
    transition: none;
  }
}
</style>
