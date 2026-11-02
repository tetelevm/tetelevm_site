<script setup>
defineProps({
  name: { type: String, required: true },
  role: { type: String, required: true },
  about: { type: String, required: true },
  lookingForWork: { type: Boolean, default: false },
  photoUrl: { type: String, default: null },
  availabilityText: { type: String, default: "" },
  photoPlaceholder: { type: String, default: "" },
})
</script>

<template>
  <section class="profile-intro" aria-labelledby="profile-name">
    <div class="profile-intro__portrait">
      <img v-if="photoUrl" class="profile-intro__photo" :src="photoUrl" :alt="name" />
      <div v-else class="profile-intro__placeholder">
        <span class="profile-intro__initial" aria-hidden="true">{{ name.slice(0, 1) }}</span>
        <span>{{ photoPlaceholder }}</span>
      </div>
    </div>
    <div class="profile-intro__body">
      <h1 id="profile-name" class="profile-intro__name">{{ name }}</h1>
      <div class="profile-intro__role-line">
        <p class="profile-intro__role"><i>{{ role }}</i></p>
        <span v-if="lookingForWork" class="profile-intro__availability">
          <span class="profile-intro__check" aria-hidden="true">✓</span>
          {{ availabilityText }}
        </span>
      </div>
      <p class="profile-intro__about">{{ about }}</p>
    </div>
  </section>
</template>

<style scoped>
.profile-intro {
  display: flow-root;
}

.profile-intro__portrait {
  float: left;
  width: 11rem;
  margin: 0 2rem 1rem 0;
  aspect-ratio: 1;
  overflow: hidden;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-medium);
  background: var(--color-surface);
}

.profile-intro__photo {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-intro__placeholder {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  color: var(--color-muted);
  font-family: var(--font-caption);
  font-size: 0.65rem;
}

.profile-intro__initial {
  color: var(--color-accent);
  font-family: var(--font-heading);
  font-size: 5rem;
  line-height: 1;
}

.profile-intro__name {
  margin: 0 0 0.9rem;
  font-family: var(--font-heading);
  font-size: clamp(2rem, 3vw, 3rem);
  font-weight: 500;
  line-height: 1.05;
  overflow-wrap: anywhere;
}

.profile-intro__role-line {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.75rem 1rem;
}

.profile-intro__role {
  margin: 0;
  color: color-mix(in srgb, var(--color-text) 60%, var(--color-muted));
  font-size: 1.25rem;
}

.profile-intro__availability {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  color: var(--color-accent);
  font-family: var(--font-caption);
  font-size: 0.72rem;
}

.profile-intro__check {
  display: grid;
  place-items: center;
  width: 1.1rem;
  height: 1.1rem;
  border: 1px solid currentColor;
  border-radius: 0.2rem;
}

.profile-intro__about {
  margin: 1.4rem 0 0;
  color: var(--color-muted);
  font-size: 0.96rem;
  line-height: 1.8;
  overflow-wrap: anywhere;
}

@media (max-width: 600px) {
  .profile-intro__portrait {
    float: none;
    width: 8rem;
    margin: 0 0 1.5rem;
  }
}
</style>
