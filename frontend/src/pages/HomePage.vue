<script setup>
import { ref, watch } from "vue"
import LanguageSwitch from "../components/common/LanguageSwitch.vue"
import MainLayout from "../components/layout/MainLayout.vue"
import { setPageMeta } from "../utils/pageMeta.js"

const language = ref("ru")

const constructionMessage = {
  ru: "Роботы-муравьишки строят эту страницу, но пока не закончили",
  en: "Tiny ant robots are building this page, but they haven't finished yet",
}

const pageDescription = {
  ru: "Личный сайт и архив проектов tetelevm.",
  en: "The personal website and project archive of tetelevm.",
}

watch(
  language,
  (value) => {
    setPageMeta({
      title: "tetelevm",
      socialTitle: "tetelevm - Main",
      description: pageDescription[value],
      path: "/",
      language: value,
    })
  },
  { immediate: true },
)
</script>

<template>
  <MainLayout active-page="home" :language="language">
    <template #header-action>
      <LanguageSwitch v-model="language" />
    </template>

    <section class="home-placeholder" aria-labelledby="home-placeholder-title">
      <p class="home-placeholder__workers" aria-hidden="true">🐜 · 🐜 · 🐜</p>
      <h1 id="home-placeholder-title" class="home-placeholder__title">
        {{ constructionMessage[language] }}
      </h1>
    </section>
  </MainLayout>
</template>

<style scoped>
.home-placeholder {
  min-height: min(28rem, 58vh);
  display: grid;
  align-content: center;
  justify-items: center;
  gap: 1.25rem;
  text-align: center;
}

.home-placeholder__workers {
  margin: 0;
  color: var(--color-accent);
  font-size: clamp(1.25rem, 3vw, 1.75rem);
  letter-spacing: 0.35em;
}

.home-placeholder__title {
  max-width: 18ch;
  margin: 0;
  font-family: var(--font-heading);
  font-size: clamp(2rem, 7vw, 4.25rem);
  font-weight: 500;
  line-height: 1.03;
  text-wrap: balance;
}
</style>
