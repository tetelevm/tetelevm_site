<script setup>
import { ref } from "vue"
import LanguageSwitch from "../components/common/LanguageSwitch.vue"
import MainLayout from "../components/layout/MainLayout.vue"

const language = ref("ru")
</script>

<template>
  <MainLayout active-page="home">
    <template #header-action>
      <LanguageSwitch v-model="language" />
    </template>

    <h1 class="visually-hidden">Главная</h1>
  </MainLayout>
</template>
