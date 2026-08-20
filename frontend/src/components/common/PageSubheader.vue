<script setup>
const statusLabels = {
  paused: "на паузе",
  closed: "завершён",
}

defineProps({
  backTo: {
    type: String,
    required: true,
  },
  backLabel: {
    type: String,
    required: true,
  },
  meta: {
    type: String,
    default: "",
  },
  status: {
    type: String,
    default: "open",
  },
  description: {
    type: String,
    default: "",
  },
})
</script>

<template>
  <div class="page-subheader">
    <div class="page-subheader__toolbar">
      <RouterLink :to="backTo">{{ backLabel }}</RouterLink>
      <span v-if="meta || statusLabels[status]" class="page-subheader__meta">
        <span v-if="meta">{{ meta }}</span>
        <span
          v-if="statusLabels[status]"
          class="page-subheader__status"
          :class="`page-subheader__status--${status}`"
        >{{ statusLabels[status] }}</span>
      </span>
    </div>
    <p v-if="description" class="page-subheader__description">
      {{ description }}
    </p>
  </div>
</template>

<style scoped>
.page-subheader__toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.page-subheader__toolbar a,
.page-subheader__toolbar span {
  color: var(--color-muted);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-decoration: none;
  text-transform: uppercase;
}

.page-subheader__meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.page-subheader__status::before {
  margin-right: 0.5rem;
  color: var(--color-muted);
  content: "·";
}

.page-subheader__meta .page-subheader__status--paused {
  color: #f0c878;
}

.page-subheader__meta .page-subheader__status--closed {
  color: #e2675b;
}

.page-subheader__toolbar a:hover,
.page-subheader__toolbar a:focus-visible {
  color: var(--color-accent);
  outline: none;
}

.page-subheader__description {
  max-width: 42rem;
  margin: 2rem 0 0;
  color: var(--color-text);
  font-size: clamp(1.2rem,2vw,1.2rem);
  line-height: 1.5;
  white-space: pre-line;
}
</style>
