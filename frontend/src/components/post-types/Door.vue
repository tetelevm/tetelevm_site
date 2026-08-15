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
  gap: 1rem;
}

.door-post__photo {
  max-width: 100%;
  max-height: 75vh;
  display: block;
  object-fit: contain;
}

.door-post__caption {
  margin: 0;
  color: #f4f4f4;
  font-size: clamp(1rem, 2.5vw, 1.25rem);
  line-height: 1.4;
  text-align: center;
}
</style>
