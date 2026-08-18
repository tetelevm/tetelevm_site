<script setup>
import PostImage from "../blocks/PostImage.vue"
import PostLayout from "../blocks/PostLayout.vue"

defineProps({
  post: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <PostLayout spacing="compact" align="center">
    <figure v-if="post.mainFile?.link" class="plasticine-post__figure plasticine-post__figure--main">
      <PostImage
        :src="post.mainFile.linkFull || post.mainFile.link"
        :full-src="post.mainFile.linkFull"
        :alt="post.name || post.text"
        lightbox
      />
    </figure>

    <figure
      v-for="(file, index) in post.files"
      :key="file.id ?? index"
      class="plasticine-post__figure"
    >
      <PostImage
        v-if="file.link"
        :src="file.linkFull || file.link"
        :full-src="file.linkFull"
        :alt="`${post.name || 'Пластилинка'} — дополнительное фото ${index + 1}`"
        lightbox
      />
    </figure>
  </PostLayout>
</template>

<style scoped>
.plasticine-post__figure {
  width: 100%;
  margin: 0;
}

.plasticine-post__figure--main {
  padding-bottom: clamp(1rem, 2.5vw, 1.5rem);
  border-bottom: 1px solid var(--color-line);
}

</style>
