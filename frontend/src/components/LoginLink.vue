<template>
  <RouterLink class="login-link" to="/login/" aria-label="Войти">
    <svg
      class="login-link__icon"
      viewBox="0 0 24 24"
      aria-hidden="true"
    >
      <path d="M10 5H6v14h4M13 8l4 4-4 4M8 12h9" />
    </svg>
  </RouterLink>
</template>

<style scoped>
.login-link {
  width: 2rem;
  height: 2rem;
  display: grid;
  border-radius: 50%;
  color: #f4f4f4;
  place-items: center;
  opacity: 0.48;
  transition:
    background-color 160ms ease,
    opacity 160ms ease;
}

.login-link:hover,
.login-link:focus-visible {
  background: rgba(255, 255, 255, 0.08);
  opacity: 0.92;
  outline: none;
}

.login-link:focus-visible {
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.7);
}

.login-link__icon {
  width: 1.2rem;
  height: 1.2rem;
  fill: none;
  stroke: currentColor;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 1.7;
}
</style>

