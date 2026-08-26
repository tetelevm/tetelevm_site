<script setup>
import { computed, ref, watch } from "vue"

import MediaFile from "./MediaFile.vue"

const props = defineProps({
  items: {
    type: Array,
    default: () => [],
  },
  label: {
    type: String,
    default: "Медиагалерея",
  },
})

const activeIndex = ref(0)
const stageAspectRatio = ref("")
const currentItem = computed(() => props.items[activeIndex.value] ?? null)
const hasReservedStage = computed(
  () => stageAspectRatio.value && ["photo", "video"].includes(
    currentItem.value?.mediaType,
  ),
)
const stageStyle = computed(() =>
  hasReservedStage.value
    ? { aspectRatio: stageAspectRatio.value }
    : undefined,
)
const isFirstItem = computed(() => activeIndex.value === 0)
const isLastItem = computed(
  () => activeIndex.value === props.items.length - 1,
)

function showPrevious() {
  if (!isFirstItem.value) {
    activeIndex.value -= 1
  }
}

function showNext() {
  if (!isLastItem.value) {
    activeIndex.value += 1
  }
}

function showItem(index) {
  activeIndex.value = index
}

function setStageAspectRatio(width, height) {
  if (width > 0 && height > 0) {
    stageAspectRatio.value = `${width} / ${height}`
  }
}

function handleDimensions({ width, height }) {
  setStageAspectRatio(width, height)
}

watch(
  () => props.items,
  () => {
    activeIndex.value = 0
    stageAspectRatio.value = ""
  },
)
</script>

<template>
  <section
    v-if="items.length"
    class="media-carousel"
    :aria-label="label"
  >
    <div
      class="media-carousel__stage"
      :style="stageStyle"
      :class="{
        'media-carousel__stage--reserved': hasReservedStage,
        'media-carousel__stage--file': currentItem
          && !['photo', 'video'].includes(currentItem.mediaType),
      }"
    >
      <MediaFile
        v-if="currentItem"
        :key="currentItem.id"
        :file="currentItem"
        :alt="`${label}: изображение ${activeIndex + 1}`"
        :lightbox="currentItem.mediaType === 'photo'"
        preview-fit="contain"
        :preserve-aspect-ratio="!hasReservedStage"
        loading="eager"
        @dimensions="handleDimensions"
      />
    </div>

    <div v-if="items.length > 1" class="media-carousel__controls">
      <button
        type="button"
        aria-label="Предыдущее медиа"
        :disabled="isFirstItem"
        @click="showPrevious"
      >
        ←
      </button>
      <div class="media-carousel__dots" aria-label="Выбор медиа">
        <button
          v-for="(item, index) in items"
          :key="item.id ?? index"
          type="button"
          :class="{ 'media-carousel__dot--active': index === activeIndex }"
          :aria-label="`Медиа ${index + 1}`"
          :aria-current="index === activeIndex ? 'true' : undefined"
          @click="showItem(index)"
        />
      </div>
      <span>{{ activeIndex + 1 }} / {{ items.length }}</span>
      <button
        type="button"
        aria-label="Следующее медиа"
        :disabled="isLastItem"
        @click="showNext"
      >
        →
      </button>
    </div>
  </section>
</template>

<style scoped>
.media-carousel {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.media-carousel__stage {
  display: grid;
  overflow: hidden;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-medium);
  background: #0d0e0c;
  box-shadow: var(--shadow-card);
  place-items: center;
}

.media-carousel__stage--file {
  min-height: 12rem;
}

.media-carousel__stage :deep(.media-file),
.media-carousel__stage :deep(video) {
  width: 100%;
}

.media-carousel__stage--reserved :deep(.media-file),
.media-carousel__stage--reserved :deep(video) {
  height: 100%;
}

.media-carousel__controls {
  display: grid;
  grid-template-columns: auto 1fr auto auto;
  align-items: center;
  gap: 0.75rem;
}

.media-carousel__controls > button {
  width: 2.4rem;
  height: 2.4rem;
  display: grid;
  padding: 0;
  border: 1px solid var(--color-line);
  border-radius: 50%;
  color: var(--color-text);
  background: var(--color-surface);
  cursor: pointer;
  place-items: center;
}

.media-carousel__controls > button:not(:disabled):hover,
.media-carousel__controls > button:not(:disabled):focus-visible {
  border-color: var(--color-accent);
  color: var(--color-accent);
  outline: none;
}

.media-carousel__controls > button:disabled {
  opacity: 0.35;
  cursor: default;
}

.media-carousel__controls > span {
  color: var(--color-muted);
  font-size: 0.75rem;
  font-variant-numeric: tabular-nums;
}

.media-carousel__dots {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.45rem;
}

.media-carousel__dots button {
  width: 0.55rem;
  height: 0.55rem;
  padding: 0;
  border: 0;
  border-radius: 50%;
  background: var(--color-line);
  cursor: pointer;
}

.media-carousel__dots button:hover,
.media-carousel__dots button:focus-visible,
.media-carousel__dots .media-carousel__dot--active {
  background: var(--color-accent);
  outline: none;
}

@media (max-width: 480px) {
  .media-carousel__controls {
    gap: 0.5rem;
  }
}
</style>
