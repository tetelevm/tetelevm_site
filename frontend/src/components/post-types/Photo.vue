<script setup>
defineProps({
  post: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <article class="photo-post">
    <img
      v-if="post.mainFile?.link"
      :src="post.mainFile.linkFull || post.mainFile.link"
      :alt="post.name || post.text"
    />
  </article>
</template>

<style scoped>
.photo-post {
  display: flex;
  justify-content: center;
}

.photo-post img {
  width: auto;
  max-width: 100%;
  height: auto;
  max-height: 85vh;
  display: block;
  border-radius: var(--radius-small);
  box-shadow: var(--shadow-card);
  object-fit: contain;
}
</style>
