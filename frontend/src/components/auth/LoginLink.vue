<script setup>
import { onMounted } from "vue"

import { authState, loadSession, logout } from "../../api/auth.js"

async function logoutUser() {
  try {
    await logout()
    window.location.assign("/archive/")
  } catch {
    window.location.reload()
  }
}

onMounted(async () => {
  if (!authState.isLoaded) {
    try {
      await loadSession()
    } catch {
      authState.isLoaded = true
    }
  }
})
</script>

<template>
  <button
    v-if="authState.isAuthenticated"
    class="login-link"
    type="button"
    :aria-label="`Выйти (${authState.username})`"
    @click="logoutUser"
  >
    <svg
      class="login-link__icon login-link__icon--logout"
      viewBox="0 0 24 24"
      aria-hidden="true"
    >
      <path d="M10 5H6v14h4M13 8l4 4-4 4M8 12h9" />
    </svg>
  </button>
  <RouterLink v-else class="login-link" to="/login/" aria-label="Войти">
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
  width: 2.4rem;
  height: 2.4rem;
  display: grid;
  padding: 0;
  border: 1px solid var(--color-line);
  border-radius: 50%;
  color: var(--color-muted);
  background: var(--color-surface);
  place-items: center;
  cursor: pointer;
  transition:
    color 160ms ease,
    border-color 160ms ease,
    background-color 160ms ease;
}

.login-link__icon--logout {
  transform: scaleX(-1);
}

.login-link:hover,
.login-link:focus-visible {
  border-color: rgba(215, 240, 111, 0.55);
  color: var(--color-accent);
  background: var(--color-surface-raised);
  outline: none;
}

.login-link:focus-visible {
  box-shadow: 0 0 0 2px var(--color-bg), 0 0 0 4px var(--color-accent);
}

.login-link__icon {
  width: 1.15rem;
  height: 1.15rem;
  fill: none;
  stroke: currentColor;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 1.7;
}
</style>
