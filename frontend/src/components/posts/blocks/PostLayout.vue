<script setup>
import { computed } from "vue"

import PostHeader from "./PostHeader.vue"

const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
  spacing: {
    type: String,
    default: "normal",
    validator: (value) => ["compact", "normal", "loose"].includes(value),
  },
  align: {
    type: String,
    default: "stretch",
    validator: (value) => ["stretch", "center"].includes(value),
  },
})

const hasSubtitle = computed(() =>
  Boolean(props.post.extra?.original_title || props.post.extra?.subtitle),
)
const hasRating = computed(() => props.post.extra?.rating != null)
</script>

<template>
  <article
    class="post-layout"
    :class="[
      `post-layout--${spacing}`,
      `post-layout--align-${align}`,
    ]"
  >
    <div class="post-layout__heading">
      <PostHeader
        :title="post.name"
        :date="post.date"
        :subtitle="post.extra?.original_title"
        :title-suffix="post.extra?.subtitle"
        :rating="hasRating ? post.extra.rating : null"
        :title-size="hasSubtitle ? 'compact' : 'normal'"
        :divided="hasSubtitle"
      />
      <slot name="header-extra" />
    </div>
    <slot />
  </article>
</template>

<style scoped>
.post-layout {
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.post-layout__heading {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
}

.post-layout__heading:empty {
  display: none;
}

.post-layout--compact {
  gap: clamp(0.75rem, 2vw, 1.25rem);
}

.post-layout--normal {
  gap: clamp(1.75rem, 4vw, 2.75rem);
}

.post-layout--loose {
  gap: clamp(2rem, 5vw, 3.5rem);
}

.post-layout--align-center {
  align-items: center;
}
</style>
