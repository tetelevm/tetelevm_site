<script setup>
defineProps({
  url: { type: String, default: null },
  previewUrl: { type: String, default: null },
  title: { type: String, default: "" },
  description: { type: String, default: "" },
  pending: { type: String, default: "" },
})
</script>

<template>
  <section class="profile-resume" aria-labelledby="resume-title">
    <component
      :is="url ? 'a' : 'span'"
      class="profile-resume__file"
      :href="url || undefined"
      :target="url ? '_blank' : undefined"
      :rel="url ? 'noopener noreferrer' : undefined"
      :aria-label="url ? title : undefined"
      :aria-hidden="url ? undefined : true"
    >
      <img v-if="previewUrl" class="profile-resume__preview" :src="previewUrl" alt="" />
      <template v-else>PDF</template>
    </component>
    <div class="profile-resume__body">
      <h2 id="resume-title" class="profile-resume__title">
        <a v-if="url" class="profile-resume__title-link" :href="url" target="_blank" rel="noopener noreferrer">{{ title }}</a>
        <template v-else>{{ title }}</template>
      </h2>
      <p class="profile-resume__description">
        {{ description }}
      </p>
      <p v-if="!url" class="profile-resume__pending">{{ pending }}</p>
    </div>
  </section>
</template>

<style scoped>
.profile-resume {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: clamp(1.25rem, 4vw, 2rem);
  border: 1px solid var(--color-line);
  border-radius: var(--radius-medium);
  background: var(--color-surface);
}

.profile-resume__file {
  display: grid;
  place-items: center;
  flex: 0 0 3.5rem;
  height: 4.5rem;
  overflow: hidden;
  border: 1px solid var(--color-accent);
  border-radius: var(--radius-small);
  color: var(--color-accent);
  font-family: var(--font-caption);
  font-size: 0.85rem;
  text-decoration: none;
}

.profile-resume__preview {
  display: block;
  width: 100%;
  height: 100%;
  min-height: 0;
  border-radius: inherit;
  object-fit: contain;
  background: var(--color-surface-raised);
}

.profile-resume__body {
  min-width: 0;
}

.profile-resume__title {
  margin: 0;
  font-family: var(--font-heading);
  font-size: 1.5rem;
  font-weight: 500;
}

.profile-resume__description,
.profile-resume__pending {
  margin: 0.65rem 0 0;
  color: var(--color-muted);
  font-size: 0.85rem;
  line-height: 1.6;
}

.profile-resume__pending {
  font-family: var(--font-caption);
  font-size: 0.7rem;
}

.profile-resume__title-link {
  color: inherit;
  text-decoration: none;
  text-underline-offset: 0.2em;
}

.profile-resume__title-link:hover {
  color: var(--color-accent);
  text-decoration: underline;
}

.profile-resume__file[href]:hover {
  background: var(--color-surface-raised);
}

.profile-resume__file[href]:focus-visible,
.profile-resume__title-link:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 4px;
}

@media (max-width: 380px) {
  .profile-resume {
    align-items: flex-start;
    gap: 1rem;
  }
}
</style>
