<script setup>
const props = defineProps({
  activePage: {
    type: String,
    default: "",
  },
  language: {
    type: String,
    default: "ru",
  },
})

const navigationText = {
  ru: {
    label: "Основная навигация",
    home: "главная",
    projects: "архив",
  },
  en: {
    label: "Main navigation",
    home: "home",
    projects: "archive",
  },
}
</script>

<template>
  <header class="site-header">
    <nav
      class="site-header__nav"
      :aria-label="navigationText[props.language].label"
    >
      <RouterLink
        class="site-header__link"
        :class="{ 'site-header__link--active': activePage === 'home' }"
        to="/"
      >
        {{ navigationText[props.language].home }}
      </RouterLink>
      <RouterLink
        class="site-header__link"
        :class="{ 'site-header__link--active': activePage === 'projects' }"
        to="/archive/"
      >
        {{ navigationText[props.language].projects }}
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
  z-index: 2;
  width: min(100% - 2rem, 800px);
  min-height: 5rem;
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid var(--color-line);
  margin-inline: auto;
}

.site-header__nav {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.site-header__link {
  position: relative;
  padding: 0.55rem 0.8rem;
  border-radius: 999px;
  color: var(--color-muted);
  font-size: 0.82rem;
  font-weight: 650;
  letter-spacing: 0.09em;
  text-decoration: none;
  text-transform: uppercase;
  transition:
    color 160ms ease,
    background-color 160ms ease;
}

.site-header__link:hover,
.site-header__link:focus-visible {
  color: var(--color-text);
  background: rgba(238, 234, 222, 0.06);
  outline: none;
}

.site-header__link--active {
  color: #151612;
  background: var(--color-accent);
}

.site-header__link--active:hover,
.site-header__link--active:focus-visible {
  color: #151612;
  background: #e2f58f;
}

.site-header__action {
  justify-self: end;
}

@media (max-width: 420px) {
  .site-header__link {
    padding-inline: 0.6rem;
    font-size: 0.73rem;
  }
}
</style>
