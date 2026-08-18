<script setup>
import { computed } from "vue"

import PostCardList from "../lists/PostCardList.vue"

const props = defineProps({
  posts: {
    type: Array,
    default: () => [],
  },
})

const items = computed(() =>
  props.posts.map((post) => ({
    key: post.id ?? post.number,
    link: post.link,
    image: post.mainFile?.link,
    label: post.name,
    rating: post.rating,
    alt: post.name,
  })),
)
</script>

<template>
  <PostCardList :items="items" />
</template>
