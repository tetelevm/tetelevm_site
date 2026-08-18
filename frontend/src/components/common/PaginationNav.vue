<script setup>
defineProps({
  currentPage: {
    type: Number,
    required: true,
  },
  totalPages: {
    type: Number,
    required: true,
  },
  label: {
    type: String,
    default: "Страницы",
  },
})

const emit = defineEmits(["select"])
</script>

<template>
  <nav v-if="totalPages > 1" class="pagination-nav" :aria-label="label">
    <button
      v-for="page in totalPages"
      :key="page"
      class="pagination-nav__page"
      :class="{ 'pagination-nav__page--active': page === currentPage }"
      type="button"
      :aria-current="page === currentPage ? 'page' : undefined"
      @click="emit('select', page)"
    >
      {{ page }}
    </button>
  </nav>
</template>

<style scoped>
.pagination-nav {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.4rem;
  margin-top: 3.5rem;
}

.pagination-nav__page {
  min-width: 2.4rem;
  padding: 0.5rem 0.65rem;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-small);
  color: var(--color-muted);
  background: var(--color-surface);
  cursor: pointer;
}

.pagination-nav__page:hover,
.pagination-nav__page:focus-visible,
.pagination-nav__page--active {
  border-color: rgba(215, 240, 111, 0.6);
  color: var(--color-text);
  outline: none;
}

.pagination-nav__page--active {
  border-color: var(--color-accent);
  color: #151612;
  background: var(--color-accent);
}
</style>
