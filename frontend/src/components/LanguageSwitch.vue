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
  align-items: baseline;
  gap: 0.25rem;
  color: #f4f4f4;
  font-size: clamp(0.9rem, 1.4vw, 1.1rem);
  line-height: 1;
}

.language-switch__option {
  padding: 0.15rem;
  border: 0;
  color: inherit;
  background: transparent;
  cursor: pointer;
  opacity: 0.42;
  transition: opacity 160ms ease;
}

.language-switch__option:hover,
.language-switch__option:focus-visible,
.language-switch__option--active {
  opacity: 0.9;
}

.language-switch__option:focus-visible {
  outline: 1px solid rgba(255, 255, 255, 0.72);
  outline-offset: 2px;
}

.language-switch__divider {
  opacity: 0.35;
}
</style>

