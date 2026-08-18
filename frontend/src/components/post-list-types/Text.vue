<script setup>
import { computed } from "vue"

import PostRowList from "../PostRowList.vue"

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
    label: post.name,
    date: post.date,
    alt: post.name,
  })),
)
</script>

<template>
  <PostRowList :items="items" />
</template>
