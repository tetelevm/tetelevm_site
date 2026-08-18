<script setup>
import { onMounted, ref } from "vue"
import { useRouter } from "vue-router"

import { authState, loadSession, login as loginUser } from "../api/auth.js"
import MainLayout from "../components/layout/MainLayout.vue"

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
    await router.push("/projects/")
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
      await router.replace("/projects/")
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
  padding: clamp(1rem, 4vw, 3rem) 0 4rem;
}

.login-form {
  width: min(100%, 25rem);
  display: flex;
  flex-direction: column;
  gap: 1.15rem;
  padding: clamp(1.5rem, 5vw, 2.5rem);
  border: 1px solid var(--color-line);
  border-radius: var(--radius-medium);
  background: rgba(29, 31, 25, 0.82);
  box-shadow: var(--shadow-card);
  backdrop-filter: blur(1rem);
}

.login-form__title {
  margin: 0 0 0.8rem;
  color: var(--color-text);
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(2rem, 7vw, 3rem);
  font-weight: 400;
  line-height: 1;
}

.login-form__field {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  color: var(--color-muted);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.login-form__field input {
  width: 100%;
  padding: 0.85rem 0.95rem;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-small);
  color: var(--color-text);
  background: var(--color-bg);
  outline: none;
  transition:
    border-color 160ms ease,
    background-color 160ms ease;
}

.login-form__field input:focus {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px rgba(215, 240, 111, 0.1);
}

.login-form__error {
  min-height: 1.1rem;
  margin: -0.35rem 0;
  color: var(--color-danger);
  font-size: 0.82rem;
  text-align: center;
}

.login-form__submit {
  width: 100%;
  padding: 0.85rem 1.4rem;
  border: 1px solid var(--color-accent);
  border-radius: var(--radius-small);
  color: #151612;
  background: var(--color-accent);
  font-size: 0.8rem;
  font-weight: 750;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  cursor: pointer;
  transition:
    border-color 160ms ease,
    background-color 160ms ease;
}

.login-form__submit:hover,
.login-form__submit:focus-visible {
  background: #e2f58f;
  outline: none;
}

.login-form__submit:focus-visible {
  box-shadow: 0 0 0 3px var(--color-bg), 0 0 0 5px var(--color-accent);
}

.login-form__submit:disabled {
  cursor: wait;
  opacity: 0.6;
}
</style>
