<script setup>
defineProps({
  activePage: {
    type: String,
    default: "",
  },
})
</script>

<template>
  <header class="site-header">
    <nav class="site-header__nav" aria-label="Основная навигация">
      <RouterLink
        class="site-header__link"
        :class="{ 'site-header__link--active': activePage === 'home' }"
        to="/"
      >
        главная
      </RouterLink>
      <span class="site-header__divider" aria-hidden="true">/</span>
      <RouterLink
        class="site-header__link"
        :class="{ 'site-header__link--active': activePage === 'projects' }"
        to="/projects/"
      >
        проекты
      </RouterLink>
    </nav>

    <div class="site-header__action">
      <slot name="action" />
    </div>
  </header>
</template>

<style scoped>
.site-header {
  position: relative;
  z-index: 1;
  min-height: 7rem;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: start;
  padding: 1.65rem clamp(1.25rem, 3.5vw, 4rem) 2.8rem;
  background: linear-gradient(
    to bottom,
    #000 0%,
    rgba(0, 0, 0, 0.92) 55%,
    rgba(0, 0, 0, 0) 100%
  );
}

.site-header__nav {
  grid-column: 2;
  display: flex;
  align-items: baseline;
  gap: clamp(0.65rem, 1.2vw, 1.1rem);
  font-size: clamp(1.6rem, 2.5vw, 2.45rem);
  font-weight: 700;
  line-height: 1;
}

.site-header__link,
.site-header__divider {
  color: #f4f4f4;
}

.site-header__link {
  text-decoration: none;
  opacity: 0.78;
  transition: opacity 160ms ease;
}

.site-header__link:hover,
.site-header__link:focus-visible,
.site-header__link--active {
  opacity: 1;
}

.site-header__divider {
  transform: rotate(9deg);
  font-size: 1.2em;
}

.site-header__action {
  grid-column: 3;
  justify-self: end;
}

@media (max-width: 640px) {
  .site-header {
    min-height: 6rem;
    grid-template-columns: 1fr auto;
    align-items: start;
    padding: 1.4rem 1rem 2.5rem;
  }

  .site-header__nav {
    grid-column: 1;
    justify-self: start;
  }

  .site-header__action {
    grid-column: 2;
  }
}
</style>
