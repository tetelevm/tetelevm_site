<script setup>
import { ref, watch } from "vue"

import LanguageSwitch from "../components/common/LanguageSwitch.vue"
import MainLayout from "../components/layout/MainLayout.vue"
import { setPageMeta } from "../utils/pageMeta.js"

const language = ref("ru")

const pageText = {
  ru: {
    eyebrow: "ошибка 404",
    title: "Здесь ничего не нашлось",
    description: "Но всегда можно посмотреть случайный пост из архива.",
    randomPost: "случайный пост →",
  },
  en: {
    eyebrow: "error 404",
    title: "Nothing was found here",
    description: "But you can always watch a random post from the archive.",
    randomPost: "get a random post →",
  },
}


watch(
  language,
  (value) => {
    const text = pageText[value]
    setPageMeta({
      title: text.title,
      socialTitle: `tetelevm - ${text.title}`,
      description: text.description,
      language: value,
      noindex: true,
      canonical: false,
    })
  },
  { immediate: true },
)
</script>

<template>
  <MainLayout :language="language">
    <template #header-action>
      <LanguageSwitch v-model="language" />
    </template>

    <section class="not-found" aria-labelledby="not-found-title">
      <p class="not-found__eyebrow">{{ pageText[language].eyebrow }}</p>
      <h1 id="not-found-title" class="not-found__title">
        {{ pageText[language].title }}
      </h1>
      <p class="not-found__description">
        {{ pageText[language].description }}
      </p>
      <RouterLink class="not-found__random" to="/archive/random/">
        {{ pageText[language].randomPost }}
      </RouterLink>
    </section>
  </MainLayout>
</template>

<style scoped>
.not-found {
  min-height: min(30rem, 62vh);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  gap: 1.2rem;
}

.not-found__eyebrow {
  margin: 0;
  color: var(--color-accent);
  font-size: 0.78rem;
  font-weight: 750;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.not-found__title {
  max-width: 14ch;
  margin: 0;
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(2.6rem, 9vw, 5.5rem);
  font-weight: 500;
  line-height: 0.98;
  text-wrap: balance;
}

.not-found__description {
  max-width: 34rem;
  margin: 0;
  color: var(--color-muted);
  font-size: clamp(1rem, 2.5vw, 1.2rem);
  line-height: 1.6;
}

.not-found__random {
  width: fit-content;
  padding: 0.75rem 1rem;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-small);
  color: var(--color-text);
  background: var(--color-surface);
  font-weight: 700;
  text-decoration: none;
  transition:
    border-color 160ms ease,
    color 160ms ease,
    background-color 160ms ease;
}

.not-found__random:hover,
.not-found__random:focus-visible {
  border-color: var(--color-accent);
  color: #151612;
  background: var(--color-accent);
  outline: none;
}
</style>
