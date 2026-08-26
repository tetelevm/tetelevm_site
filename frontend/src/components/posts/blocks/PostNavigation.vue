<script setup>
const MAX_LABEL_LENGTH = 80

const props = defineProps({
  projectName: {
    type: String,
    required: true,
  },
  previousPost: {
    type: Object,
    default: null,
  },
  nextPost: {
    type: Object,
    default: null,
  },
})

function fullPostLabel(post) {
  return `${props.projectName} #${post.number}: ${post.label}`
}

function shortenedPostLabel(post) {
  const characters = Array.from(String(post.label ?? ""))
  const label = characters.length <= MAX_LABEL_LENGTH
    ? characters.join("")
    : `${characters.slice(0, MAX_LABEL_LENGTH - 3).join("").trimEnd()}...`
  return `${props.projectName} #${post.number}: ${label}`
}
</script>

<template>
  <nav
    v-if="previousPost || nextPost"
    class="post-navigation"
    aria-label="Соседние посты"
  >
    <RouterLink
      v-if="nextPost"
      class="post-navigation__link post-navigation__link--next"
      :to="nextPost.link"
      :aria-label="`Следующий пост: ${fullPostLabel(nextPost)}`"
    >
      <span class="post-navigation__arrow" aria-hidden="true">←</span>
      <span class="post-navigation__text">
        {{ shortenedPostLabel(nextPost) }}
      </span>
    </RouterLink>

    <RouterLink
      v-if="previousPost"
      class="post-navigation__link post-navigation__link--previous"
      :to="previousPost.link"
      :aria-label="`Предыдущий пост: ${fullPostLabel(previousPost)}`"
    >
      <span class="post-navigation__text">
        {{ shortenedPostLabel(previousPost) }}
      </span>
      <span class="post-navigation__arrow" aria-hidden="true">→</span>
    </RouterLink>
  </nav>
</template>

<style scoped>
.post-navigation {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
  padding-top: 1.25rem;
  border-top: 1px solid var(--color-line);
}

.post-navigation__link {
  min-width: 0;
  display: flex;
  align-items: flex-start;
  gap: 0.55rem;
  padding: 0.85rem 0.95rem;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-small);
  color: var(--color-muted);
  background: var(--color-surface);
  font-family: var(--font-text);
  font-size: clamp(0.9rem, 2.5vw, 1.05rem);
  line-height: 1.4;
  text-decoration: none;
}

.post-navigation__text {
  min-width: 0;
  hyphens: auto;
  overflow-wrap: anywhere;
  word-break: break-word;
}

.post-navigation__link--previous {
  grid-column: 2;
  justify-content: flex-end;
  text-align: right;
}

.post-navigation__arrow {
  flex: 0 0 auto;
  padding-top: 0.08rem;
  color: var(--color-accent);
  font-weight: 750;
  line-height: 1.4;
}

.post-navigation__link:hover,
.post-navigation__link:focus-visible {
  border-color: var(--color-accent);
  color: var(--color-text);
  background: var(--color-surface-raised);
  outline: none;
}

.post-navigation__link:focus-visible {
  box-shadow: 0 0 0 2px var(--color-bg), 0 0 0 4px var(--color-accent);
}

.post-navigation__link:hover .post-navigation__arrow,
.post-navigation__link:focus-visible .post-navigation__arrow {
  transform: translateX(-0.18rem);
}

.post-navigation__link--next:hover .post-navigation__arrow,
.post-navigation__link--next:focus-visible .post-navigation__arrow {
  transform: translateX(0.18rem);
}

@media (max-width: 520px) {
  .post-navigation {
    grid-template-columns: 1fr;
  }

  .post-navigation__link--previous {
    grid-column: 1;
  }
}

@media (prefers-reduced-motion: no-preference) {
  .post-navigation__link {
    transition:
      border-color 160ms ease,
      color 160ms ease,
      background-color 160ms ease;
  }

  .post-navigation__arrow {
    transition: transform 160ms ease;
  }
}
</style>
