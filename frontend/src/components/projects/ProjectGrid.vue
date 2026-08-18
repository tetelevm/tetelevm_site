<script setup>
import ProjectCard from "./ProjectCard.vue"

defineProps({
  projects: {
    type: Array,
    required: true,
  },
})
</script>

<template>
  <div class="project-grid">
    <ProjectCard
      v-for="project in projects"
      :key="project.id"
      :title="project.title"
      :href="project.href"
      :image="project.image"
      :accent="project.accent"
      :is-private="project.isPrivate"
      :status="project.status"
    />
  </div>
</template>

<style scoped>
.project-grid {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: clamp(1rem, 2.5vw, 1.5rem);
}

@media (max-width: 820px) {
  .project-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 520px) {
  .project-grid {
    width: min(100%, 24rem);
    margin-inline: auto;
    grid-template-columns: 1fr;
  }
}
</style>
