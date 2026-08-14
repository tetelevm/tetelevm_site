<script setup>
import { onMounted, ref } from "vue"
import { useRouter } from "vue-router"

import { authState, loadSession, login as loginUser } from "../api/auth.js"
import MainLayout from "../components/MainLayout.vue"

const router = useRouter()
const username = ref("")
const password = ref("")
const errorMessage = ref("")
const isSubmitting = ref(false)

async function submitLogin() {
  errorMessage.value = ""
  isSubmitting.value = true

  try {
    await loginUser(username.value, password.value)
    await router.push("/content/")
  } catch (error) {
    errorMessage.value =
      error.message === "Invalid credentials"
        ? "неверные данные"
        : "не удалось войти"
  } finally {
    isSubmitting.value = false
  }
}

onMounted(async () => {
  try {
    if (!authState.isLoaded) {
      await loadSession()
    }
    if (authState.isAuthenticated) {
      await router.replace("/content/")
    }
  } catch {
    errorMessage.value = "не удалось проверить сессию"
  }
})
</script>

<template>
  <MainLayout>
    <div class="login-page__content">
      <form class="login-form" novalidate @submit.prevent="submitLogin">
        <h1 class="login-form__title">вход</h1>

        <label class="login-form__field">
          <span>логин</span>
          <input
            v-model="username"
            name="username"
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
          v-if="errorMessage"
          class="login-form__error"
          role="alert"
        >
          {{ errorMessage }}
        </p>

        <button
          class="login-form__submit"
          type="submit"
          :disabled="isSubmitting"
        >
          {{ isSubmitting ? "входим…" : "войти" }}
        </button>
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
