<script setup>
defineProps({
  backTo: {
    type: String,
    required: true,
  },
  backLabel: {
    type: String,
    required: true,
  },
  meta: {
    type: String,
    default: "",
  },
  description: {
    type: String,
    default: "",
  },
})
</script>

<template>
  <div class="page-subheader">
    <div class="page-subheader__toolbar">
      <RouterLink :to="backTo">{{ backLabel }}</RouterLink>
      <span v-if="meta">{{ meta }}</span>
    </div>
    <p v-if="description" class="page-subheader__description">
      {{ description }}
    </p>
  </div>
</template>

<style scoped>
.page-subheader__toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.page-subheader__toolbar a,
.page-subheader__toolbar span {
  color: var(--color-muted);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-decoration: none;
  text-transform: uppercase;
}

.page-subheader__toolbar a:hover,
.page-subheader__toolbar a:focus-visible {
  color: var(--color-accent);
  outline: none;
}

.page-subheader__description {
  max-width: 42rem;
  margin: 0.75rem 0 0;
  color: var(--color-text);
  font-size: clamp(0.9rem, 2vw, 1rem);
  line-height: 1.5;
  white-space: pre-line;
}
</style>
