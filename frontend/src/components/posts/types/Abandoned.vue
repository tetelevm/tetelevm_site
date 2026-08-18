<script setup>
import { computed } from "vue"

import MediaCarousel from "../../media/MediaCarousel.vue"
import PlainPostText from "../blocks/PlainPostText.vue"
import PostLayout from "../blocks/PostLayout.vue"
import RatedPostHeader from "../blocks/RatedPostHeader.vue"

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

function coordinateText(value) {
  if (typeof value === "number" && Number.isFinite(value)) {
    return String(value)
  }
  return typeof value === "string" ? value.trim() : ""
}

const locationLabel = computed(() => {
  const latitude = coordinateText(props.post.extra?.location?.latitude)
  const longitude = coordinateText(props.post.extra?.location?.longitude)
  return latitude && longitude ? `${latitude}, ${longitude}` : ""
})

const locationHref = computed(() => {
  const value = props.post.extra?.location?.link
  if (typeof value !== "string" || !value.trim()) {
    return ""
  }

  const candidate = value.trim()
  const normalized = /^[a-z][a-z\d+.-]*:/i.test(candidate)
    ? candidate
    : `https://${candidate}`
  try {
    const url = new URL(normalized)
    return ["http:", "https:"].includes(url.protocol) ? url.href : ""
  } catch {
    return ""
  }
})

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
  <PostLayout>
    <div class="abandoned-post__heading">
      <RatedPostHeader :title="post.name" :rating="post.extra?.rating" />
      <a
        v-if="locationLabel && locationHref"
        class="abandoned-post__location"
        :href="locationHref"
        target="_blank"
        rel="noopener noreferrer"
      >
        {{ locationLabel }}
      </a>
    </div>

    <PlainPostText :text="post.text" />

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
  </PostLayout>
</template>

<style scoped>
.abandoned-post__heading {
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
}

.abandoned-post__location {
  width: fit-content;
  color: var(--color-accent);
  font-size: 0.88rem;
  font-variant-numeric: tabular-nums;
  text-decoration-color: rgba(215, 240, 111, 0.48);
  text-underline-offset: 0.22em;
}

.abandoned-post__location:hover,
.abandoned-post__location:focus-visible {
  color: var(--color-text);
  text-decoration-color: var(--color-accent);
  outline: none;
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
