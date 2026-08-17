<script setup>
defineProps({
  files: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <ul v-if="files.length" class="post-file-list" aria-label="Файлы">
    <li v-for="file in files" :key="file.id">
      <a :href="file.linkFull || file.link">
        <span>{{ file.name || "файл" }}</span>
        <span aria-hidden="true">↗</span>
      </a>
    </li>
  </ul>
</template>

<style scoped>
.post-file-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0;
  margin: 0;
  list-style: none;
}

.post-file-list a {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.75rem 0.9rem;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-small);
  color: var(--color-muted);
  background: var(--color-surface);
  font-size: 0.82rem;
  overflow-wrap: anywhere;
  text-decoration: none;
}

.post-file-list a:hover,
.post-file-list a:focus-visible {
  border-color: rgba(215, 240, 111, 0.55);
  color: var(--color-accent);
  outline: none;
}
</style>
