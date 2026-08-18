<script setup>
import { computed } from "vue"

import MediaCarousel from "../MediaCarousel.vue"
import RatedPostHeader from "../RatedPostHeader.vue"

const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
})

const criteria = computed(() => [
  { label: "уникальность", value: props.post.extra?.uniqueness },
  { label: "монументальность", value: props.post.extra?.monumentality },
  { label: "атмосфера", value: props.post.extra?.atmosphere },
  { label: "жизненность", value: props.post.extra?.liveliness },
])

function normalizedRating(value) {
  const rating = Number.parseInt(value, 10)
  return Number.isFinite(rating) ? Math.min(5, Math.max(1, rating)) : null
}

function ratingHouses(value) {
  const rating = normalizedRating(value)
  return rating === null ? "—" : "🏚".repeat(rating)
}
</script>

<template>
  <article class="abandoned-post">
    <RatedPostHeader :title="post.name" :rating="post.extra?.rating" />

    <div v-if="post.text" class="abandoned-post__text">{{ post.text }}</div>

    <dl class="abandoned-post__criteria">
      <div v-for="criterion in criteria" :key="criterion.label">
        <dt>{{ criterion.label }}:</dt>
        <dd
          :aria-label="normalizedRating(criterion.value) === null
            ? 'оценка не указана'
            : `${normalizedRating(criterion.value)} из 5`"
        >
          {{ ratingHouses(criterion.value) }}
        </dd>
      </div>
    </dl>

    <MediaCarousel :items="post.files" :label="`Галерея: ${post.name}`" />
  </article>
</template>

<style scoped>
.abandoned-post {
  display: flex;
  flex-direction: column;
  gap: clamp(1.75rem, 4vw, 2.75rem);
}

.abandoned-post__text {
  color: var(--color-text);
  font-size: 1.2rem;
  line-height: 1.75;
  white-space: pre-line;
}

.abandoned-post__criteria {
  display: flex;
  flex-direction: column;
  gap: 0;
  border-top: 1px solid var(--color-line);
  margin: 0;
}

.abandoned-post__criteria > div {
  display: grid;
  grid-template-columns: minmax(9rem, 1fr) minmax(8rem, auto);
  align-items: center;
  gap: 1rem;
  padding: 0.9rem 0;
  border-bottom: 1px solid var(--color-line);
}

.abandoned-post__criteria dt {
  color: var(--color-muted);
  font-size: 0.78rem;
  font-weight: 750;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.abandoned-post__criteria dd {
  margin: 0;
  font-size: clamp(1rem, 3vw, 1.3rem);
  letter-spacing: 0.08em;
  text-align: right;
  white-space: nowrap;
}

@media (max-width: 480px) {
  .abandoned-post__criteria > div {
    grid-template-columns: 1fr;
    gap: 0.4rem;
  }

  .abandoned-post__criteria dd {
    text-align: left;
  }
}
</style>
