<script setup>
import LoginLink from "./LoginLink.vue"

defineProps({
  projectName: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <div class="project-header-action">
    <span class="project-header-action__name">{{ projectName }}</span>
    <LoginLink />
  </div>
</template>

<style scoped>
.project-header-action {
  min-width: 0;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 2em;
}

.project-header-action__name {
  max-width: min(18rem, 35vw);
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
  .project-header-action__name {
    max-width: 30vw;
    font-size: 0.8rem;
  }
}
</style>
