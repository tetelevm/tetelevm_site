<script setup>
defineProps({
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
</script>

<template>
  <article
    class="post-layout"
    :class="[
      `post-layout--${spacing}`,
      `post-layout--align-${align}`,
    ]"
  >
    <slot />
  </article>
</template>

<style scoped>
.post-layout {
  display: flex;
  flex-direction: column;
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
