<script setup>
import { computed, ref, watch } from "vue"

import LightboxImage from "./LightboxImage.vue"

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
const currentItem = computed(() => props.items[activeIndex.value] ?? null)

function showPrevious() {
  activeIndex.value =
    (activeIndex.value - 1 + props.items.length) % props.items.length
}

function showNext() {
  activeIndex.value = (activeIndex.value + 1) % props.items.length
}

function showItem(index) {
  activeIndex.value = index
}

watch(
  () => props.items,
  () => {
    activeIndex.value = 0
  },
)
</script>

<template>
  <section
    v-if="items.length"
    class="media-carousel"
    :aria-label="label"
    tabindex="0"
    @keydown.left.prevent="showPrevious"
    @keydown.right.prevent="showNext"
  >
    <div
      class="media-carousel__stage"
      :class="{
        'media-carousel__stage--file': currentItem
          && !['photo', 'video'].includes(currentItem.mediaType),
      }"
    >
      <LightboxImage
        v-if="currentItem?.mediaType === 'photo'"
        :key="currentItem.id"
        :preview-src="currentItem.link"
        :full-src="currentItem.linkFull"
        :alt="`${label}: изображение ${activeIndex + 1}`"
        preview-fit="contain"
        preserve-aspect-ratio
      />
      <video
        v-else-if="currentItem?.mediaType === 'video'"
        :key="currentItem.id"
        :src="currentItem.linkFull || currentItem.link"
        controls
        preload="metadata"
      />
      <a
        v-else-if="currentItem"
        class="media-carousel__file"
        :href="currentItem.linkFull || currentItem.link"
      >
        открыть файл
      </a>
    </div>

    <div v-if="items.length > 1" class="media-carousel__controls">
      <button type="button" aria-label="Предыдущее медиа" @click="showPrevious">
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
      <button type="button" aria-label="Следующее медиа" @click="showNext">
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
  outline: none;
}

.media-carousel:focus-visible .media-carousel__stage {
  box-shadow: 0 0 0 2px var(--color-bg), 0 0 0 4px var(--color-accent);
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

.media-carousel__stage video {
  width: 100%;
  height: auto;
  display: block;
  object-fit: contain;
}

.media-carousel__file {
  color: var(--color-accent);
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

.media-carousel__controls > button:hover,
.media-carousel__controls > button:focus-visible {
  border-color: var(--color-accent);
  color: var(--color-accent);
  outline: none;
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
