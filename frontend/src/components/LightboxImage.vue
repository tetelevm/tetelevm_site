<script setup>
import { nextTick, onBeforeUnmount, ref } from "vue"

const props = defineProps({
  previewSrc: {
    type: String,
    required: true,
  },
  fullSrc: {
    type: String,
    default: "",
  },
  alt: {
    type: String,
    default: "",
  },
})

const dialog = ref(null)
const isOpen = ref(false)
let previousBodyOverflow = ""

async function openImage() {
  isOpen.value = true
  previousBodyOverflow = document.body.style.overflow
  document.body.style.overflow = "hidden"
  await nextTick()
  dialog.value?.showModal()
}

function closeImage() {
  dialog.value?.close()
}

function finishClosing() {
  isOpen.value = false
  document.body.style.overflow = previousBodyOverflow
}

function closeOnBackdrop(event) {
  if (event.target === event.currentTarget) {
    closeImage()
  }
}

onBeforeUnmount(() => {
  document.body.style.overflow = previousBodyOverflow
})
</script>

<template>
  <button class="lightbox-image__trigger" type="button" @click="openImage">
    <img :src="previewSrc" :alt="alt" loading="lazy" />
  </button>

  <dialog
    v-if="isOpen"
    ref="dialog"
    class="lightbox-image__dialog"
    aria-label="Полноразмерное изображение"
    @click="closeOnBackdrop"
    @close="finishClosing"
  >
    <button
      class="lightbox-image__close"
      type="button"
      aria-label="Закрыть изображение"
      @click="closeImage"
    >
      ×
    </button>
    <img
      class="lightbox-image__full"
      :src="fullSrc || previewSrc"
      :alt="alt"
    />
  </dialog>
</template>

<style scoped>
.lightbox-image__trigger {
  width: 100%;
  height: 100%;
  display: block;
  padding: 0;
  border: 0;
  color: inherit;
  background: transparent;
  cursor: zoom-in;
}

.lightbox-image__trigger img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}

.lightbox-image__trigger:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: -2px;
}

.lightbox-image__dialog {
  width: 100vw;
  max-width: none;
  height: 100vh;
  max-height: none;
  padding: clamp(2.75rem, 6vw, 4.5rem);
  border: 0;
  margin: 0;
  color: var(--color-text);
  background: rgba(10, 11, 9, 0.96);
  cursor: zoom-out;
}

.lightbox-image__dialog::backdrop {
  background: rgba(10, 11, 9, 0.96);
}

.lightbox-image__full {
  width: auto;
  max-width: 100%;
  height: auto;
  max-height: 100%;
  display: block;
  margin: auto;
  object-fit: contain;
  cursor: default;
}

.lightbox-image__close {
  position: fixed;
  z-index: 1;
  top: 0.75rem;
  right: 0.9rem;
  width: 2.5rem;
  height: 2.5rem;
  display: grid;
  padding: 0;
  border: 1px solid rgba(238, 234, 222, 0.35);
  border-radius: 50%;
  color: var(--color-text);
  background: rgba(29, 31, 25, 0.9);
  cursor: pointer;
  font-size: 1.75rem;
  line-height: 1;
  place-items: center;
}

.lightbox-image__close:hover,
.lightbox-image__close:focus-visible {
  border-color: var(--color-accent);
  color: var(--color-accent);
  outline: none;
}
</style>
