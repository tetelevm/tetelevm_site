<script setup>
defineProps({
  post: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <article class="door-post">
    <img
      v-if="post.mainFile?.link"
      class="door-post__photo"
      :src="post.mainFile.link"
      :alt="post.text"
    />
    <p class="door-post__caption">{{ post.text }}</p>
  </article>
</template>

<style scoped>
.door-post {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.25rem;
}

.door-post__photo {
  max-width: 100%;
  max-height: 75vh;
  display: block;
  border-radius: var(--radius-small);
  box-shadow: var(--shadow-card);
  object-fit: contain;
}

.door-post__caption {
  margin: 0;
  color: var(--color-text);
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(1rem, 2.5vw, 1.25rem);
  line-height: 1.45;
  text-align: center;
}
</style>
