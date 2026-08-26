<script setup>
import MediaFile from "../../media/MediaFile.vue"

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
  mediaType: {
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
    <MediaFile
      :src="src"
      :full-src="fullSrc"
      :media-type="mediaType"
      :alt="alt"
      :lightbox="lightbox"
      preview-fit="contain"
      :preserve-aspect-ratio="variant === 'stage'"
    />
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

.post-image--natural :deep(.media-file),
.post-image--natural :deep(.media-file > img),
.post-image--natural :deep(.media-file > video),
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

.post-image--natural :deep(.media-file--audio),
.post-image--natural :deep(.media-file--other) {
  width: 100%;
}

.post-image--stage {
  overflow: hidden;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-medium);
  background: #0d0e0c;
  box-shadow: var(--shadow-card);
}

.post-image--stage :deep(.media-file),
.post-image--stage :deep(.media-file > img),
.post-image--stage :deep(.media-file > video) {
  width: 100%;
  height: auto;
  display: block;
  object-fit: contain;
}
</style>
