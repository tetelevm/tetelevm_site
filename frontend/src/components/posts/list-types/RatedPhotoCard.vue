<script setup>
import { computed } from "vue"

import PostCardList from "./PostCardList.vue"

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
    image: post.cardFile?.mediaType === "photo" ? post.cardFile.link : "",
    label: post.label,
    rating: post.rating,
    alt: post.label,
  })),
)
</script>

<template>
  <PostCardList :items="items" />
</template>
