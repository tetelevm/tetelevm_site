<script setup>
defineProps({
  post: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <article class="plasticine-post">
    <figure v-if="post.mainFile?.link" class="plasticine-post__figure plasticine-post__figure--main">
      <img :src="post.mainFile.link" :alt="post.name || post.text" />
    </figure>

    <figure
      v-for="(file, index) in post.files"
      :key="file.id ?? index"
      class="plasticine-post__figure"
    >
      <img
        v-if="file.link"
        :src="file.link"
        :alt="`${post.name || 'Пластилинка'} — дополнительное фото ${index + 1}`"
        loading="lazy"
      />
    </figure>
  </article>
</template>

<style scoped>
.plasticine-post {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: clamp(1.5rem, 4vw, 2.75rem);
}

.plasticine-post__figure {
  width: 100%;
  margin: 0;
}

.plasticine-post__figure img {
  width: auto;
  max-width: 100%;
  max-height: 85vh;
  display: block;
  border-radius: var(--radius-small);
  margin-inline: auto;
  box-shadow: var(--shadow-card);
}

.plasticine-post__figure--main {
  padding: clamp(0.55rem, 1.5vw, 0.9rem);
  border: 1px solid var(--color-line);
  border-radius: var(--radius-medium);
  background: var(--color-surface-raised);
  box-shadow: var(--shadow-card);
}

.plasticine-post__figure--main img {
  box-shadow: none;
}

</style>
