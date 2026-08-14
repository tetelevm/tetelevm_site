<script setup>
import AppHeader from "./AppHeader.vue"

defineProps({
  activePage: {
    type: String,
    default: "",
  },
})
</script>

<template>
  <div class="main-layout">
    <AppHeader :active-page="activePage">
      <template #action>
        <slot name="header-action" />
      </template>
    </AppHeader>

    <main class="main-layout__content">
      <slot />
    </main>
  </div>
</template>

<style scoped>
.main-layout {
  min-height: 100vh;
  background: #202020;
}

.main-layout__content {
  width: min(100% - 2rem, 800px);
  margin-inline: auto;
  padding-block: clamp(0.7rem, 1.7vw, 1.6rem) 5rem;
}
</style>
