<script setup>
defineProps({
  projectName: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <span class="project-header-action">{{ projectName }}</span>
</template>

<style scoped>
.project-header-action {
  min-width: 0;
  max-width: min(18rem, 35vw);
  display: block;
  overflow: hidden;
  color: #cbd59a;
  font-size: 1.8rem;
  font-weight: 650;
  letter-spacing: 0.075em;
  line-height: 1.1;
  text-overflow: ellipsis;
  text-transform: uppercase;
  white-space: nowrap;
}

@media (max-width: 480px) {
  .project-header-action {
    max-width: 30vw;
    font-size: 0.8rem;
  }
}
</style>
