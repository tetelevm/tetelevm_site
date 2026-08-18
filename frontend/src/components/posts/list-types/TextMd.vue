<script setup>
import { computed } from "vue"

import PostRowList from "../lists/PostRowList.vue"

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
    image: post.mainFile?.mediaType === "photo" ? post.mainFile.link : "",
    label: post.label,
    date: post.date,
    alt: post.label,
  })),
)
</script>

<template>
  <PostRowList :items="items" />
</template>
