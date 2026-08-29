<script setup>
import { computed } from "vue"

const props = defineProps({
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

const paginationItems = computed(() => {
  const totalPages = Math.max(1, Math.trunc(props.totalPages))
  const currentPage = Math.min(
    totalPages,
    Math.max(1, Math.trunc(props.currentPage)),
  )
  const visiblePages = new Set()

  for (let page = 1; page <= Math.min(3, totalPages); page += 1) {
    visiblePages.add(page)
  }
  for (
    let page = Math.max(1, currentPage - 2);
    page <= Math.min(totalPages, currentPage + 2);
    page += 1
  ) {
    visiblePages.add(page)
  }
  for (let page = Math.max(1, totalPages - 2); page <= totalPages; page += 1) {
    visiblePages.add(page)
  }

  const pages = [...visiblePages].sort((left, right) => left - right)
  const items = []
  pages.forEach((page, index) => {
    const previousPage = pages[index - 1]
    if (previousPage !== undefined && page - previousPage > 1) {
      items.push({ key: `gap-${previousPage}-${page}`, page: null })
    }
    items.push({ key: `page-${page}`, page })
  })
  return items
})
</script>

<template>
  <nav v-if="totalPages > 1" class="pagination-nav" :aria-label="label">
    <template v-for="item in paginationItems" :key="item.key">
      <span
        v-if="item.page === null"
        class="pagination-nav__ellipsis"
        aria-hidden="true"
      >…</span>
      <button
        v-else
        class="pagination-nav__page"
        :class="{
          'pagination-nav__page--active': item.page === currentPage,
        }"
        type="button"
        :aria-current="item.page === currentPage ? 'page' : undefined"
        @click="emit('select', item.page)"
      >
        {{ item.page }}
      </button>
    </template>
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

.pagination-nav__ellipsis {
  min-width: 1.5rem;
  display: grid;
  color: var(--color-muted);
  place-items: center;
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
