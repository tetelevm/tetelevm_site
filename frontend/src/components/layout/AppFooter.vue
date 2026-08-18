<script setup>
const props = defineProps({
  language: {
    type: String,
    default: "ru",
  },
})

const currentYear = new Date().getFullYear()

const footerText = {
  ru: `Это футер. А сейчас ${currentYear} год.`,
  en: `This is the footer. The year is ${currentYear}.`,
}
</script>

<template>
  <footer class="app-footer">
    <p>{{ footerText[props.language] }}</p>
  </footer>
</template>

<style scoped>
.app-footer {
  position: relative;
  width: min(100% - 2rem, 800px);
  margin-inline: auto;
  padding: 1.25rem 0 1.75rem;
  border-top: 1px solid rgba(255, 255, 255, 0.09);
  color: rgba(216, 217, 207, 0.42);
  text-align: center;
  font-size: 0.95rem;
}

.app-footer p {
  margin: 0;
}
</style>
