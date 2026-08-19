<script setup>
import { computed } from "vue"
import MarkdownIt from "markdown-it"

const props = defineProps({
  source: {
    type: String,
    default: "",
  },
})

const markdown = new MarkdownIt({
  breaks: true,
  html: false,
  linkify: true,
  typographer: true,
})

const rendered = computed(() => markdown.render(props.source))
</script>

<template>
  <div class="markdown-content" v-html="rendered" />
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
</style>
