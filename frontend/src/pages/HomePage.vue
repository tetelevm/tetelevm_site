<script setup>
import { ref } from "vue"
import LanguageSwitch from "../components/LanguageSwitch.vue"
import MainLayout from "../components/MainLayout.vue"

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
