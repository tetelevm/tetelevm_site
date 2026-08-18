<script setup>
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
    <h1>{{ title }}</h1>
    <span v-if="date" class="dated-post-header__date">{{ date }}</span>
  </header>
</template>

<style scoped>
.dated-post-header {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: end;
  gap: 1.5rem;
}

.dated-post-header h1 {
  grid-column: 1;
  margin: 0;
  color: var(--color-text);
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(1.8rem, 5vw, 3rem);
  font-weight: 500;
  line-height: 1.1;
  overflow-wrap: anywhere;
  text-align: left;
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
