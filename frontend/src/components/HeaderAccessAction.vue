<script setup>
import { onBeforeUnmount, ref } from "vue"

import logoUrl from "../assets/site-logo.png"
import LoginLink from "./LoginLink.vue"

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

onBeforeUnmount(() => window.clearTimeout(resetTimer))
</script>

<template>
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
</template>

<style scoped>
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
