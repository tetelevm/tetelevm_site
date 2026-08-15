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
      <span v-if="isPrivate" class="project-card__shade" aria-hidden="true" />
    </span>
  </RouterLink>
</template>

<style scoped>
.project-card {
  position: relative;
  display: block;
  color: #fff;
  border: 3px solid rgba(255, 255, 255, 0.62);
  border-radius: 2px;
  text-decoration: none;
  transition:
    transform 180ms ease,
    border-color 180ms ease,
    box-shadow 180ms ease;
}

.project-card::after {
  position: absolute;
  inset: -3px;
  z-index: 2;
  border: 4px solid transparent;
  border-radius: 2px;
  content: "";
  pointer-events: none;
}

.project-card:hover,
.project-card:focus-visible {
  z-index: 2;
  border-color: rgba(255, 255, 255, 0.88);
  outline: none;
  transform: translateY(-0.3rem);
}

.project-card:focus-visible {
  box-shadow: 0 0 0 3px #202020, 0 0 0 5px #fff;
}

.project-card__frame {
  position: relative;
  display: grid;
  overflow: hidden;
  grid-template-rows: auto minmax(4rem, auto);
  background: #202020;
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
}

.project-card__placeholder {
  color: rgba(20, 20, 20, 0.78);
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
  padding: 0.35rem 0.8rem;
  place-items: center;
  overflow: hidden;
  font-size: clamp(1.15rem, 2.2vw, 2rem);
  font-weight: 700;
  line-height: 1.05;
  text-align: center;
  text-overflow: ellipsis;
}

.project-card--private {
  color: rgba(255, 255, 255, 0.68);
}

.project-card--private::after {
  border-right-color: rgba(204, 88, 88, 0.55);
  border-bottom-color: rgba(204, 88, 88, 0.55);
  box-shadow: 4px 4px 10px rgba(160, 45, 45, 0.16);
}

.project-card__shade {
  position: absolute;
  inset: 0;
  z-index: 0;
  background: linear-gradient(
    135deg,
    rgba(110, 110, 110, 0.18) 0%,
    rgba(110, 110, 110, 0.18) 49.6%,
    rgba(91, 91, 91, 0) 50.2%,
    rgba(91, 91, 91, 0) 100%
  );
  pointer-events: none;
}

@media (prefers-reduced-motion: reduce) {
  .project-card {
    transition: none;
  }
}
</style>
