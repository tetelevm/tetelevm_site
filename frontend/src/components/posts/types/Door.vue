<script setup>
import PlainPostText from "../blocks/PlainPostText.vue"
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
  <PostLayout :post="post" spacing="compact" align="center">
    <PostImage
      :src="post.mainFile?.link"
      :full-src="post.mainFile?.linkFull"
      :media-type="post.mainFile?.mediaType"
      :alt="post.text"
      max-height="75vh"
    />
    <PlainPostText :text="post.text" align="center" />
  </PostLayout>
</template>
