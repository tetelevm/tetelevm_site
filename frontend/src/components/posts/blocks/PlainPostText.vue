<script setup>
defineProps({
  text: {
    type: String,
    default: "",
  },
  align: {
    type: String,
    default: "left",
    validator: (value) => ["left", "center"].includes(value),
  },
})
</script>

<template>
  <div
    v-if="text"
    class="plain-post-text"
    :class="`plain-post-text--${align}`"
  >
    {{ text }}
  </div>
</template>

<style scoped>
.plain-post-text {
  color: var(--color-text);
  font-size: 1.2rem;
  line-height: 1.65;
  white-space: pre-line;
}

.plain-post-text--center {
  text-align: center;
}
</style>
