<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue"

import { authState, loadSession } from "../../api/auth.js"
import logoUrl from "../../assets/site-logo.png"
import LoginLink from "./LoginLink.vue"

const props = defineProps({
  language: {
    type: String,
    default: "ru",
  },
})

const REQUIRED_PRESSES = 3
const PRESS_WINDOW_MS = 700

const isAccessVisible = ref(false)
let pressCount = 0
let resetTimer

function activateLogo() {
  window.clearTimeout(resetTimer)
  pressCount += 1

  if (pressCount >= REQUIRED_PRESSES) {
    isAccessVisible.value = true
    pressCount = 0
    return
  }

  resetTimer = window.setTimeout(() => {
    pressCount = 0
  }, PRESS_WINDOW_MS)
}

const adminLabel = {
  ru: "Открыть админку",
  en: "Open admin",
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

onBeforeUnmount(() => window.clearTimeout(resetTimer))
</script>

<template>
  <div class="header-access-actions">
    <a
      v-if="authState.isStaff"
      class="header-access-actions__admin"
      href="/_admin/"
      :aria-label="adminLabel[props.language]"
      :title="adminLabel[props.language]"
    >
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M4 20l4.2-1 10.9-10.9a2.1 2.1 0 0 0-3-3L5.2 16 4 20Z" />
        <path d="m14.8 6.4 2.8 2.8" />
      </svg>
    </a>

    <LoginLink v-if="isAccessVisible" />
    <button
      v-else
      class="header-access-action"
      type="button"
      aria-label="Логотип сайта"
      @click="activateLogo"
    >
      <img :src="logoUrl" alt="" />
    </button>
  </div>
</template>

<style scoped>
.header-access-actions {
  display: flex;
  align-items: center;
  gap: 0.55rem;
}

.header-access-actions__admin {
  width: 2.4rem;
  height: 2.4rem;
  display: grid;
  padding: 0;
  border: 1px solid var(--color-line);
  border-radius: 50%;
  color: var(--color-muted);
  background: var(--color-surface);
  place-items: center;
  transition:
    color 160ms ease,
    border-color 160ms ease,
    background-color 160ms ease;
}

.header-access-actions__admin:hover,
.header-access-actions__admin:focus-visible {
  border-color: rgba(215, 240, 111, 0.55);
  color: var(--color-accent);
  background: var(--color-surface-raised);
  outline: none;
}

.header-access-actions__admin:focus-visible {
  box-shadow: 0 0 0 2px var(--color-bg), 0 0 0 4px var(--color-accent);
}

.header-access-actions__admin svg {
  width: 1.1rem;
  height: 1.1rem;
  fill: none;
  stroke: currentColor;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 1.7;
}

.header-access-action {
  width: 2.6rem;
  height: 2.6rem;
  flex: 0 0 auto;
  display: grid;
  overflow: hidden;
  padding: 0;
  border: 0;
  border-radius: 50%;
  background: transparent;
  cursor: pointer;
  place-items: center;
}

.header-access-action img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: contain;
}

.header-access-action:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 3px;
}
</style>
