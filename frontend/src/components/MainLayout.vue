<script setup>
import AppHeader from "./AppHeader.vue"
import HeaderAccessAction from "./HeaderAccessAction.vue"

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
        <div class="main-layout__header-action">
          <slot name="header-action" />
          <HeaderAccessAction />
        </div>
      </template>
    </AppHeader>

    <div v-if="$slots.subheader" class="main-layout__subheader">
      <slot name="subheader" />
    </div>

    <main class="main-layout__content">
      <slot />
    </main>
  </div>
</template>

<style scoped>
.main-layout {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  background:
    radial-gradient(circle at 12% -10%, rgba(215, 240, 111, 0.08), transparent 28rem),
    var(--color-bg);
}

.main-layout__header-action {
  min-width: 0;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 2em;
}

.main-layout::before {
  position: fixed;
  inset: 0;
  background-image: linear-gradient(
    rgba(255, 255, 255, 0.012) 1px,
    transparent 1px
  );
  background-size: 100% 4rem;
  content: "";
  pointer-events: none;
}

.main-layout__content {
  position: relative;
  width: min(100% - 2rem, 800px);
  margin-inline: auto;
  padding-block: clamp(2rem, 5vw, 4.5rem) 6rem;
}

.main-layout__subheader {
  position: relative;
  width: min(100% - 2rem, 800px);
  margin-inline: auto;
  padding-top: 1rem;
}

.main-layout__subheader + .main-layout__content {
  padding-top: clamp(1.5rem, 3vw, 2.5rem);
}
</style>
