<script setup>
defineProps({
  posts: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <div class="plasticine-list">
    <RouterLink
      v-for="post in posts"
      :key="post.id ?? post.number"
      class="plasticine-card"
      :to="post.link"
      :aria-label="post.name || post.text || `Пластилинка ${post.number}`"
    >
      <span class="plasticine-card__frame">
        <img
          v-if="post.mainFile?.link"
          :src="post.mainFile.link"
          :alt="post.name || post.text"
        />
        <span v-else class="plasticine-card__empty">нет фото</span>
      </span>
    </RouterLink>
  </div>
</template>

<style scoped>
.plasticine-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: clamp(1.5rem, 5vw, 3.5rem);
  align-items: start;
}

.plasticine-card {
  min-width: 0;
  display: block;
  padding: clamp(0.55rem, 1.5vw, 0.8rem);
  border: 1px solid rgba(238, 234, 222, 0.18);
  border-radius: 0.35rem 0.65rem 0.4rem 0.75rem;
  color: var(--color-muted);
  background:
    linear-gradient(145deg, rgba(255, 255, 255, 0.045), transparent 55%),
    var(--color-surface-raised);
  box-shadow:
    0 0 0 0.3rem var(--color-surface),
    var(--shadow-card);
  text-decoration: none;
  transform: rotate(-0.35deg);
  transition:
    border-color 160ms ease,
    box-shadow 180ms ease,
    transform 180ms ease;
}

.plasticine-card:nth-child(even) {
  transform: rotate(0.35deg);
}

.plasticine-card__frame {
  min-height: 10rem;
  display: grid;
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.45);
  border-radius: var(--radius-small);
  background: #10110e;
  place-items: center;
}

.plasticine-card img {
  width: 100%;
  height: auto;
  display: block;
}

.plasticine-card__empty {
  padding: 4rem 1rem;
  font-size: 0.75rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.plasticine-card:hover,
.plasticine-card:focus-visible {
  border-color: rgba(215, 240, 111, 0.65);
  box-shadow:
    0 0 0 0.3rem var(--color-surface),
    0 1.5rem 3.5rem rgba(0, 0, 0, 0.35);
  outline: none;
  transform: rotate(0) translateY(-0.25rem);
}

@media (max-width: 560px) {
  .plasticine-list {
    grid-template-columns: 1fr;
  }
}
</style>
