<script setup>
import LightboxImage from "../../media/LightboxImage.vue"

defineProps({
  src: {
    type: String,
    default: "",
  },
  fullSrc: {
    type: String,
    default: "",
  },
  alt: {
    type: String,
    default: "",
  },
  lightbox: {
    type: Boolean,
    default: false,
  },
  variant: {
    type: String,
    default: "natural",
    validator: (value) => ["natural", "stage"].includes(value),
  },
  maxHeight: {
    type: String,
    default: "85vh",
  },
})
</script>

<template>
  <div
    v-if="src"
    class="post-image"
    :class="`post-image--${variant}`"
    :style="{ '--post-image-max-height': maxHeight }"
  >
    <LightboxImage
      v-if="lightbox"
      :preview-src="src"
      :full-src="fullSrc"
      :alt="alt"
      preview-fit="contain"
      :preserve-aspect-ratio="variant === 'stage'"
    />
    <img v-else :src="src" :alt="alt" />
  </div>
</template>

<style scoped>
.post-image {
  width: 100%;
}

.post-image--natural {
  display: flex;
  justify-content: center;
}

.post-image--natural > img,
.post-image--natural :deep(.lightbox-image__trigger img) {
  width: auto;
  max-width: 100%;
  height: auto;
  max-height: var(--post-image-max-height);
  display: block;
  border-radius: var(--radius-small);
  margin-inline: auto;
  box-shadow: var(--shadow-card);
  object-fit: contain;
}

.post-image--natural :deep(.lightbox-image__trigger) {
  width: auto;
  height: auto;
  display: block;
  margin-inline: auto;
}

.post-image--stage {
  overflow: hidden;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-medium);
  background: #0d0e0c;
  box-shadow: var(--shadow-card);
}

.post-image--stage > img {
  width: 100%;
  height: auto;
  display: block;
  object-fit: contain;
}
</style>
