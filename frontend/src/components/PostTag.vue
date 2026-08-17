<script setup>
defineProps({
  name: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <li class="post-tag">{{ name }}</li>
</template>

<style scoped>
.post-tag {
  padding: 0.38rem 0.65rem;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-small);
  color: var(--color-muted);
  background: var(--color-surface);
  font-size: 0.74rem;
  letter-spacing: 0.04em;
  line-height: 1.2;
}
</style>
