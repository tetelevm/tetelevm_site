<script setup>
import { formatDate } from "../../../utils/date.js"

import PostTitle from "./PostTitle.vue"

defineProps({
  title: {
    type: String,
    default: "",
  },
  date: {
    type: String,
    default: "",
  },
  subtitle: {
    type: String,
    default: "",
  },
  titleSuffix: {
    type: String,
    default: "",
  },
  rating: {
    type: [Number, String],
    default: null,
  },
  titleSize: {
    type: String,
    default: "normal",
    validator: (value) => ["compact", "normal"].includes(value),
  },
  divided: {
    type: Boolean,
    default: false,
  },
})
</script>

<template>
  <header
    v-if="title || date || subtitle || titleSuffix || rating != null"
    class="post-header"
    :class="{ 'post-header--divided': divided }"
  >
    <PostTitle
      v-if="title || subtitle || titleSuffix"
      :title="title"
      :subtitle="subtitle"
      :suffix="titleSuffix"
      :size="titleSize"
    >
      <time v-if="date" class="post-header__date" :datetime="date">
        {{ formatDate(date) }}
      </time>
    </PostTitle>
    <time v-else-if="date" class="post-header__date" :datetime="date">
      {{ formatDate(date) }}
    </time>
    <div v-if="rating != null" class="post-header__rating" aria-label="Оценка">
      {{ rating }}
    </div>
  </header>
</template>

<style scoped>
.post-header {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
}

.post-header--divided {
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--color-line);
}

.post-header__date {
  display: block;
  margin-top: 0.35rem;
  color: var(--color-muted);
  font-size: 1.25rem;
  font-variant-numeric: tabular-nums;
}

.post-header__rating {
  min-width: 3.8rem;
  min-height: 3.8rem;
  flex: 0 0 auto;
  display: grid;
  padding: 0.6rem;
  border: 1px solid rgba(215, 240, 111, 0.55);
  border-radius: 50%;
  color: var(--color-accent);
  background: var(--color-surface);
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.55rem;
  line-height: 1;
  place-items: center;
}

@media (max-width: 480px) {
  .post-header {
    align-items: flex-start;
  }

  .post-header__rating {
    min-width: 3.2rem;
    min-height: 3.2rem;
    font-size: 1.25rem;
  }
}
</style>
