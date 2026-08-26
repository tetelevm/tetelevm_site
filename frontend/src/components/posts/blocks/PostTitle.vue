<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    default: "",
  },
  suffix: {
    type: String,
    default: "",
  },
  size: {
    type: String,
    default: "normal",
    validator: (value) => ["compact", "normal"].includes(value),
  },
})
</script>

<template>
  <div class="post-title" :class="`post-title--${size}`">
    <h1>
      <span>{{ title }}</span>
      <wbr v-if="suffix" />
      <em v-if="suffix" class="post-title__suffix">{{ suffix }}</em>
    </h1>
    <slot />
    <p v-if="subtitle">{{ subtitle }}</p>
  </div>
</template>

<style scoped>
.post-title {
  min-width: 0;
}

.post-title h1 {
  margin: 0;
  overflow-wrap: anywhere;
  color: var(--color-text);
  font-family: var(--font-heading);
  font-size: clamp(1.8rem, 5vw, 3rem);
  font-weight: 500;
  line-height: 1.08;
}

.post-title--compact h1 {
  font-size: clamp(1.4rem, 4vw, 2.25rem);
}

.post-title__suffix {
  max-width: 100%;
  display: inline-block;
  margin-left: 0.45em;
  overflow-wrap: anywhere;
  color: var(--color-muted);
  font-size: 0.65em;
  font-style: italic;
  font-weight: 400;
  vertical-align: baseline;
}

.post-title p {
  margin: 0.35rem 0 0;
  color: var(--color-muted);
  font-size: clamp(0.95rem, 2.5vw, 1.1rem);
  font-style: italic;
  line-height: 1.35;
}
</style>
