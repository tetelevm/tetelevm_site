<script setup>
defineProps({
  modelValue: {
    type: String,
    default: "ru",
  },
})

const emit = defineEmits(["update:modelValue"])
</script>

<template>
  <div class="language-switch" aria-label="Выбор языка">
    <button
      class="language-switch__option"
      :class="{ 'language-switch__option--active': modelValue === 'ru' }"
      type="button"
      :aria-pressed="modelValue === 'ru'"
      @click="emit('update:modelValue', 'ru')"
    >
      ru
    </button>
    <span class="language-switch__divider" aria-hidden="true">/</span>
    <button
      class="language-switch__option"
      :class="{ 'language-switch__option--active': modelValue === 'en' }"
      type="button"
      :aria-pressed="modelValue === 'en'"
      @click="emit('update:modelValue', 'en')"
    >
      en
    </button>
  </div>
</template>

<style scoped>
.language-switch {
  display: flex;
  align-items: center;
  gap: 0.1rem;
  padding: 0.2rem;
  border: 1px solid var(--color-line);
  border-radius: 999px;
  color: var(--color-muted);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  line-height: 1;
  text-transform: uppercase;
}

.language-switch__option {
  padding: 0.38rem 0.5rem;
  border: 0;
  border-radius: 999px;
  color: inherit;
  background: transparent;
  cursor: pointer;
  transition:
    color 160ms ease,
    background-color 160ms ease;
}

.language-switch__option:hover,
.language-switch__option:focus-visible,
.language-switch__option--active {
  color: var(--color-text);
  background: var(--color-surface-raised);
}

.language-switch__option:focus-visible {
  outline: 1px solid var(--color-accent);
  outline-offset: 2px;
}

.language-switch__divider {
  display: none;
}
</style>
