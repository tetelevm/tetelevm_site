<script setup>
import { computed, ref } from "vue"
import MarkdownIt from "markdown-it"
import markdownItContainer from "markdown-it-container"

import LightboxImage from "../../media/LightboxImage.vue"

const props = defineProps({
  source: {
    type: String,
    default: "",
  },
})

const lightbox = ref(null)
const selectedImage = ref({ src: "", alt: "" })

const markdown = new MarkdownIt({
  breaks: true,
  html: false,
  linkify: true,
  typographer: true,
})

markdown.use(markdownItContainer, "spoiler", {
  validate: (params) => /^spoiler(?:\s+.*)?$/.test(params.trim()),
  render: (tokens, index) => {
    if (tokens[index].nesting === 1) {
      const title = tokens[index].info.trim().slice("spoiler".length).trim()
      const safeTitle = markdown.utils.escapeHtml(title || "Спойлер")
      return `<details class="markdown-content__spoiler"><summary>${safeTitle}</summary>\n`
    }
    return "</details>\n"
  },
})

markdown.renderer.rules.image = (tokens, index, options, env, renderer) => {
  const token = tokens[index]
  const alt = renderer.renderInlineAsText(token.children, options, env)
  token.attrSet("alt", alt)
  token.attrSet("tabindex", "0")
  token.attrSet("role", "button")
  token.attrSet("aria-label", `Открыть изображение: ${alt || "без описания"}`)
  return renderer.renderToken(tokens, index, options)
}

const rendered = computed(() => markdown.render(props.source))

function markdownImage(target) {
  return target instanceof Element ? target.closest(".markdown-content img") : null
}

function openMarkdownImage(image) {
  selectedImage.value = {
    src: image.currentSrc || image.src,
    alt: image.alt,
  }
  lightbox.value?.openImage()
}

function handleImageClick(event) {
  const image = markdownImage(event.target)
  if (image) {
    event.preventDefault()
    openMarkdownImage(image)
  }
}

function handleImageKeydown(event) {
  if (!["Enter", " "].includes(event.key)) {
    return
  }
  const image = markdownImage(event.target)
  if (image) {
    event.preventDefault()
    openMarkdownImage(image)
  }
}
</script>

<template>
  <div
    class="markdown-content"
    @click="handleImageClick"
    @keydown="handleImageKeydown"
    v-html="rendered"
  />
  <LightboxImage
    ref="lightbox"
    :preview-src="selectedImage.src || '/favicon.ico'"
    :full-src="selectedImage.src"
    :alt="selectedImage.alt"
    triggerless
  />
</template>

<style scoped>
.markdown-content {
  min-width: 0;
  overflow-wrap: anywhere;
  color: var(--color-text);
  font-size: 1.2rem;
  line-height: 1.7;
  word-break: break-word;
}

.markdown-content :deep(:first-child) {
  margin-top: 0;
}

.markdown-content :deep(:last-child) {
  margin-bottom: 0;
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3),
.markdown-content :deep(h4) {
  margin: 1.8em 0 0.65em;
  color: var(--color-text);
  font-family: Georgia, "Times New Roman", serif;
  font-weight: 500;
  line-height: 1.2;
}

.markdown-content :deep(h1) {
  font-size: 2rem;
}

.markdown-content :deep(h2) {
  font-size: 1.6rem;
}

.markdown-content :deep(h3) {
  font-size: 1.3rem;
}

.markdown-content :deep(p),
.markdown-content :deep(ul),
.markdown-content :deep(ol),
.markdown-content :deep(blockquote),
.markdown-content :deep(pre),
.markdown-content :deep(table) {
  margin: 0 0 1.2em;
}

.markdown-content :deep(a) {
  color: var(--color-accent);
  text-underline-offset: 0.18em;
}

.markdown-content :deep(blockquote) {
  padding-left: 1rem;
  border-left: 3px solid var(--color-accent);
  color: var(--color-muted);
}

.markdown-content :deep(code) {
  padding: 0.12em 0.35em;
  border-radius: 0.25rem;
  background: var(--color-surface-raised);
  font-size: 0.9em;
}

.markdown-content :deep(pre) {
  overflow-x: auto;
  padding: 1rem;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-small);
  background: var(--color-surface);
}

.markdown-content :deep(pre code) {
  padding: 0;
  background: transparent;
}

.markdown-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: var(--radius-small);
  cursor: zoom-in;
}

.markdown-content :deep(img:focus-visible) {
  outline: 2px solid var(--color-accent);
  outline-offset: 0.2rem;
}

.markdown-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
}

.markdown-content :deep(th),
.markdown-content :deep(td) {
  padding: 0.55rem 0.7rem;
  border: 1px solid var(--color-line);
  text-align: left;
}

.markdown-content :deep(.markdown-content__spoiler) {
  margin: 0 0 1em;
  padding: 0.2rem 1rem;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-small);
  background: var(--color-surface);
}

.markdown-content :deep(.markdown-content__spoiler summary) {
  color: var(--color-accent);
  cursor: pointer;
  font-weight: 650;
}

.markdown-content :deep(.markdown-content__spoiler[open] summary) {
  margin-bottom: 0.8rem;
}

.markdown-content :deep(.markdown-content__spoiler summary:focus-visible) {
  outline: 2px solid var(--color-accent);
  outline-offset: 0.25rem;
}
</style>
