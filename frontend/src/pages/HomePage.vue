<script setup>
import { ref } from "vue"
import AppHeader from "../components/AppHeader.vue"
import LanguageSwitch from "../components/LanguageSwitch.vue"

const language = ref("ru")
</script>

<template>
  <div class="home-page">
    <AppHeader active-page="home">
      <template #action>
        <LanguageSwitch v-model="language" />
      </template>
    </AppHeader>

    <main>
      <h1 class="visually-hidden">Главная</h1>
    </main>
  </div>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
  background: #202020;
}
</style>

