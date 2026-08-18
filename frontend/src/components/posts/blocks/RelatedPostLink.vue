<script setup>
defineProps({
  relatedPost: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <p class="related-post-link">
    <span>related with:</span>
    <RouterLink :to="relatedPost.link">
      #{{ relatedPost.number }}
    </RouterLink>
  </p>
</template>

<style scoped>
.related-post-link {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-line);
  margin: 0;
  color: var(--color-muted);
  font-size: 0.78rem;
  letter-spacing: 0.04em;
}

.related-post-link a {
  color: var(--color-accent);
  font-weight: 700;
  text-decoration: none;
}

.related-post-link a:hover,
.related-post-link a:focus-visible {
  text-decoration: underline;
  text-underline-offset: 0.18em;
  outline: none;
}
</style>
