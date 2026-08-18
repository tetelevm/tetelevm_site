<script setup>
defineProps({
  loading: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: "",
  },
  loadingText: {
    type: String,
    default: "Загрузка…",
  },
})
</script>

<template>
  <p v-if="loading || error" class="page-status" :role="error ? 'alert' : undefined">
    {{ error || loadingText }}
  </p>
</template>

<style scoped>
.page-status {
  margin: 0;
  color: var(--color-muted);
  text-align: center;
}
</style>
