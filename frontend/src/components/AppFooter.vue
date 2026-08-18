<script setup>
const currentYear = new Date().getFullYear()
</script>

<template>
  <footer class="app-footer">
    <p>Это футер. А сейчас {{ currentYear }} год.</p>
  </footer>
</template>

<style scoped>
.app-footer {
  position: relative;
  width: min(100% - 2rem, 800px);
  margin-inline: auto;
  padding: 1.25rem 0 1.75rem;
  border-top: 1px solid rgba(255, 255, 255, 0.18);
  color: var(--color-text-muted);
  text-align: center;
  font-size: 0.8rem;
}

.app-footer p {
  margin: 0;
}
</style>
