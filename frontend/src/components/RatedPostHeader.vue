<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    default: "",
  },
  rating: {
    type: [Number, String],
    default: null,
  },
})
</script>

<template>
  <header class="rated-post-header">
    <div class="rated-post-header__titles">
      <h1>{{ title }}</h1>
      <p v-if="subtitle">{{ subtitle }}</p>
    </div>
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

.rated-post-header__titles {
  min-width: 0;
}

.rated-post-header__titles h1 {
  margin: 0;
  color: var(--color-text);
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(2rem, 6vw, 3.4rem);
  font-weight: 500;
  line-height: 1.05;
}

.rated-post-header__titles p {
  margin: 0.35rem 0 0;
  color: var(--color-muted);
  font-size: clamp(0.95rem, 2.5vw, 1.1rem);
  font-style: italic;
  line-height: 1.35;
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
