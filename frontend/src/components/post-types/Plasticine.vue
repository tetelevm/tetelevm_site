<script setup>
import LightboxImage from "../LightboxImage.vue"

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
      <LightboxImage
        :preview-src="post.mainFile.linkFull || post.mainFile.link"
        :full-src="post.mainFile.linkFull"
        :alt="post.name || post.text"
        preview-fit="contain"
      />
    </figure>

    <figure
      v-for="(file, index) in post.files"
      :key="file.id ?? index"
      class="plasticine-post__figure"
    >
      <LightboxImage
        v-if="file.link"
        :preview-src="file.linkFull || file.link"
        :full-src="file.linkFull"
        :alt="`${post.name || 'Пластилинка'} — дополнительное фото ${index + 1}`"
        preview-fit="contain"
      />
    </figure>
  </article>
</template>

<style scoped>
.plasticine-post {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: clamp(0.75rem, 2vw, 1.25rem);
}

.plasticine-post__figure {
  width: 100%;
  margin: 0;
}

.plasticine-post__figure :deep(.lightbox-image__trigger) {
  width: auto;
  height: auto;
  display: block;
  margin-inline: auto;
}

.plasticine-post__figure :deep(.lightbox-image__trigger img) {
  width: auto;
  max-width: 100%;
  height: auto;
  max-height: 85vh;
  display: block;
  border-radius: var(--radius-small);
  margin-inline: auto;
  box-shadow: var(--shadow-card);
}

.plasticine-post__figure--main {
  padding-bottom: clamp(1rem, 2.5vw, 1.5rem);
  border-bottom: 1px solid var(--color-line);
}

</style>
