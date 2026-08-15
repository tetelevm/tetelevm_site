<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  href: {
    type: String,
    required: true,
  },
  image: {
    type: String,
    default: "",
  },
  accent: {
    type: String,
    default: "#d8c65a",
  },
  isPrivate: {
    type: Boolean,
    default: false,
  },
})
</script>

<template>
  <RouterLink
    class="project-card"
    :class="{ 'project-card--private': isPrivate }"
    :to="href"
    :aria-label="`${title}${isPrivate ? ', закрытый проект' : ''}`"
  >
    <span class="project-card__frame">
      <span
        class="project-card__cover"
        :style="{ '--project-accent': accent }"
      >
        <img v-if="image" :src="image" :alt="`Обложка проекта «${title}»`" />
        <span v-else class="project-card__placeholder" aria-hidden="true">
          {{ title.slice(0, 1) }}
        </span>
      </span>

      <span class="project-card__title">{{ title }}</span>
      <span v-if="isPrivate" class="project-card__badge">закрытый</span>
      <span v-if="isPrivate" class="project-card__shade" aria-hidden="true" />
    </span>
  </RouterLink>
</template>

<style scoped>
.project-card {
  position: relative;
  display: block;
  overflow: hidden;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-medium);
  color: var(--color-text);
  background: var(--color-surface);
  text-decoration: none;
  transition:
    transform 200ms ease,
    border-color 180ms ease,
    box-shadow 180ms ease;
}

.project-card:hover,
.project-card:focus-visible {
  z-index: 2;
  border-color: rgba(215, 240, 111, 0.65);
  box-shadow: var(--shadow-card);
  outline: none;
  transform: translateY(-0.35rem);
}

.project-card:focus-visible {
  box-shadow: 0 0 0 3px var(--color-bg), 0 0 0 5px var(--color-accent);
}

.project-card__frame {
  position: relative;
  display: grid;
  overflow: hidden;
  grid-template-rows: auto minmax(3.75rem, auto);
  background: var(--color-surface);
}

.project-card__cover {
  position: relative;
  aspect-ratio: 1;
  display: grid;
  min-height: 0;
  overflow: hidden;
  place-items: center;
  background:
    radial-gradient(
      circle at 72% 20%,
      rgba(255, 255, 255, 0.25),
      transparent 28%
    ),
    linear-gradient(145deg, var(--project-accent), #5e5529);
}

.project-card__cover img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: center;
  transition: transform 350ms ease;
}

.project-card:hover .project-card__cover img,
.project-card:focus-visible .project-card__cover img {
  transform: scale(1.025);
}

.project-card__placeholder {
  color: rgba(20, 20, 20, 0.72);
  font-family: ui-sans-serif, system-ui, sans-serif;
  font-size: clamp(4rem, 10vw, 8rem);
  font-weight: 800;
  line-height: 1;
  text-transform: uppercase;
}

.project-card__title {
  z-index: 1;
  display: grid;
  min-width: 0;
  padding: 0.8rem 1rem;
  place-items: center;
  overflow: hidden;
  font-size: clamp(1rem, 2vw, 1.25rem);
  font-weight: 620;
  line-height: 1.15;
  text-align: center;
  text-overflow: ellipsis;
}

.project-card--private {
  border-color: rgba(226, 140, 124, 0.32);
}

.project-card__shade {
  position: absolute;
  inset: 0;
  z-index: 1;
  background: rgba(15, 16, 13, 0.22);
  pointer-events: none;
}

.project-card__badge {
  position: absolute;
  top: 0.65rem;
  right: 0.65rem;
  z-index: 2;
  padding: 0.3rem 0.5rem;
  border: 1px solid rgba(226, 140, 124, 0.45);
  border-radius: 999px;
  color: #f1b1a5;
  background: rgba(21, 22, 18, 0.78);
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  backdrop-filter: blur(0.4rem);
}

@media (prefers-reduced-motion: reduce) {
  .project-card {
    transition: none;
  }

  .project-card__cover img {
    transition: none;
  }
}
</style>
