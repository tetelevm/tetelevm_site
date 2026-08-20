<script setup>
import { formatDate } from "../../../utils/date.js"

import PostTitle from "./PostTitle.vue"

defineProps({
  title: {
    type: String,
    required: true,
  },
  date: {
    type: String,
    default: "",
  },
})
</script>

<template>
  <header class="dated-post-header">
    <PostTitle :title="title" />
    <time
      v-if="date"
      class="dated-post-header__date"
      :datetime="date"
    >{{ formatDate(date) }}</time>
  </header>
</template>

<style scoped>
.dated-post-header {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: end;
  gap: 1.5rem;
}

.dated-post-header__date {
  grid-column: 2;
  color: var(--color-muted);
  font-size: 0.82rem;
  font-variant-numeric: tabular-nums;
}

@media (max-width: 480px) {
  .dated-post-header {
    gap: 0.75rem;
  }
}
</style>
