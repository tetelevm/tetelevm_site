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
  <PostLayout align="center">
    <PostImage
      :src="post.mainFile?.linkFull || post.mainFile?.link"
      :alt="post.name || post.text"
    />
  </PostLayout>
</template>
