<script setup>
defineProps({
  code: {
    type: String,
    required: true,
  },
  name: {
    type: String,
    required: true,
  },
  projectCode: {
    type: String,
    required: true,
  },
  linked: {
    type: Boolean,
    default: true,
  },
})
</script>

<template>
  <li>
    <RouterLink
      v-if="linked"
      class="post-tag"
      :to="{ path: `/archive/${projectCode}/`, query: { tag: code } }"
    >
      {{ name }}
    </RouterLink>
    <span v-else class="post-tag">{{ name }}</span>
  </li>
</template>

<style scoped>
.post-tag {
  display: block;
  padding: 0.38rem 0.65rem;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-small);
  color: var(--color-muted);
  background: var(--color-surface);
  font-size: 1.1rem;
  letter-spacing: 0.04em;
  line-height: 1.2;
  text-decoration: none;
  transition:
    border-color 160ms ease,
    color 160ms ease;
}

.post-tag:hover,
.post-tag:focus-visible {
  border-color: var(--color-accent);
  color: var(--color-text);
  outline: none;
}
</style>
