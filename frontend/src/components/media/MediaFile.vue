<script setup>
import { computed } from "vue"

import { resolvedMediaType } from "../../utils/media.js"
import LightboxImage from "./LightboxImage.vue"

const props = defineProps({
  file: {
    type: Object,
    default: null,
  },
  src: {
    type: String,
    default: "",
  },
  fullSrc: {
    type: String,
    default: "",
  },
  mediaType: {
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
  previewFit: {
    type: String,
    default: "contain",
    validator: (value) => ["cover", "contain"].includes(value),
  },
  preserveAspectRatio: {
    type: Boolean,
    default: false,
  },
  loading: {
    type: String,
    default: "lazy",
    validator: (value) => ["eager", "lazy"].includes(value),
  },
})

const emit = defineEmits(["dimensions"])

const source = computed(() => props.src || props.file?.link || "")
const originalSource = computed(
  () => props.fullSrc || props.file?.linkFull || source.value,
)
const type = computed(() =>
  resolvedMediaType(props.mediaType || props.file?.mediaType, source.value),
)
const label = computed(() => props.alt || props.file?.name || "файл")

function reportImageSize(event) {
  emit("dimensions", {
    width: event.currentTarget.naturalWidth,
    height: event.currentTarget.naturalHeight,
  })
}

function reportVideoSize(event) {
  emit("dimensions", {
    width: event.currentTarget.videoWidth,
    height: event.currentTarget.videoHeight,
  })
}
</script>

<template>
  <div v-if="source" class="media-file" :class="`media-file--${type}`">
    <LightboxImage
      v-if="type === 'photo' && lightbox"
      :preview-src="source"
      :full-src="originalSource"
      :alt="label"
      :preview-fit="previewFit"
      :preserve-aspect-ratio="preserveAspectRatio"
      :loading="loading"
      @preview-load="emit('dimensions', $event)"
    />
    <img
      v-else-if="type === 'photo'"
      :src="source"
      :alt="label"
      :loading="loading"
      @load="reportImageSize"
    />
    <video
      v-else-if="type === 'video'"
      :src="originalSource"
      :aria-label="label"
      controls
      playsinline
      preload="metadata"
      @loadedmetadata="reportVideoSize"
    />
    <audio
      v-else-if="type === 'audio'"
      :src="originalSource"
      :aria-label="label"
      controls
      preload="metadata"
    />
    <a v-else :href="originalSource">{{ label }}</a>
  </div>
</template>

<style scoped>
.media-file {
  min-width: 0;
  max-width: 100%;
}

.media-file img,
.media-file video {
  width: 100%;
  height: auto;
  display: block;
  object-fit: contain;
}

.media-file audio {
  width: min(100%, 36rem);
  display: block;
}

.media-file a {
  color: var(--color-accent);
  overflow-wrap: anywhere;
}
</style>
