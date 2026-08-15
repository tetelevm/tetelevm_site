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
  gap: 1.5rem 1rem;
}

.door-card {
  min-width: 0;
  color: #f4f4f4;
  text-decoration: none;
}

.door-card__photo {
  aspect-ratio: 1;
  display: block;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.55);
  background: rgba(255, 255, 255, 0.05);
  transition:
    border-color 160ms ease,
    transform 160ms ease;
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
  font-size: 0.9rem;
  line-height: 1.25;
  text-align: center;
}

.door-card:hover .door-card__photo,
.door-card:focus-visible .door-card__photo {
  border-color: rgba(255, 255, 255, 0.9);
  transform: translateY(-0.2rem);
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
</style>
