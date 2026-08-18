<script setup>
import PostTitle from "./PostTitle.vue"

defineProps({
  title: {
    type: String,
    required: true,
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
})
</script>

<template>
  <header class="rated-post-header">
    <PostTitle
      :title="title"
      :subtitle="subtitle"
      :suffix="titleSuffix"
      :size="titleSize"
    />
    <div
      v-if="rating !== null && rating !== undefined"
      class="rated-post-header__rating"
      aria-label="Оценка"
    >
      {{ rating }}
    </div>
  </header>
</template>

<style scoped>
.rated-post-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
}

.rated-post-header__rating {
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
  .rated-post-header {
    align-items: flex-start;
  }

  .rated-post-header__rating {
    min-width: 3.2rem;
    min-height: 3.2rem;
    font-size: 1.25rem;
  }
}
</style>
