<script setup>
import { ref } from "vue"
import MainLayout from "../components/MainLayout.vue"

const login = ref("")
const password = ref("")
const hasError = ref(false)

function submitLogin() {
  hasError.value = true
}
</script>

<template>
  <MainLayout>
    <div class="login-page__content">
      <form class="login-form" novalidate @submit.prevent="submitLogin">
        <h1 class="login-form__title">вход</h1>

        <label class="login-form__field">
          <span>логин</span>
          <input
            v-model="login"
            name="login"
            type="text"
            autocomplete="username"
            required
          />
        </label>

        <label class="login-form__field">
          <span>пароль</span>
          <input
            v-model="password"
            name="password"
            type="password"
            autocomplete="current-password"
            required
          />
        </label>

        <p
          v-if="hasError"
          class="login-form__error"
          role="alert"
        >
          неверные данные
        </p>

        <button class="login-form__submit" type="submit">войти</button>
      </form>
    </div>
  </MainLayout>
</template>

<style scoped>
.login-page__content {
  display: flex;
  justify-content: center;
  padding: clamp(1.5rem, 5vw, 4rem) 0 4rem;
}

.login-form {
  width: min(100%, 22rem);
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.login-form__title {
  margin: 0 0 0.35rem;
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.75rem;
  font-weight: 600;
  text-align: center;
}

.login-form__field {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  color: rgba(255, 255, 255, 0.58);
  font-size: 0.88rem;
}

.login-form__field input {
  width: 100%;
  padding: 0.75rem 0.85rem;
  border: 1px solid rgba(255, 255, 255, 0.36);
  border-radius: 2px;
  color: #f4f4f4;
  background: rgba(0, 0, 0, 0.12);
  outline: none;
  transition:
    border-color 160ms ease,
    background-color 160ms ease;
}

.login-form__field input:focus {
  border-color: rgba(255, 255, 255, 0.72);
  background: rgba(0, 0, 0, 0.2);
}

.login-form__error {
  min-height: 1.1rem;
  margin: -0.35rem 0;
  color: rgba(223, 108, 108, 0.82);
  font-size: 0.82rem;
  text-align: center;
}

.login-form__submit {
  align-self: center;
  min-width: 8rem;
  padding: 0.65rem 1.4rem;
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 2px;
  color: rgba(255, 255, 255, 0.88);
  background: transparent;
  cursor: pointer;
  transition:
    border-color 160ms ease,
    background-color 160ms ease;
}

.login-form__submit:hover,
.login-form__submit:focus-visible {
  border-color: rgba(255, 255, 255, 0.82);
  background: rgba(255, 255, 255, 0.07);
  outline: none;
}
</style>
