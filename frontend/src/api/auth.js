import { reactive } from "vue"

export const authState = reactive({
  isAuthenticated: false,
  username: null,
  isStaff: false,
  isLoaded: false,
})

async function requestJson(path, options = {}) {
  const response = await fetch(path, {
    credentials: "same-origin",
    ...options,
  })
  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.detail || "Ошибка авторизации")
  }
  return data
}

function setAuthState(session) {
  authState.isAuthenticated = session.isAuthenticated
  authState.username = session.username ?? null
  authState.isStaff = session.isStaff ?? false
  authState.isLoaded = true
}

async function getCsrfToken() {
  const data = await requestJson("/_api/auth/csrf/")
  return data.csrfToken
}

export async function loadSession() {
  const session = await requestJson("/_api/auth/session/")
  setAuthState(session)
  return session
}

export async function login(username, password) {
  const csrfToken = await getCsrfToken()
  const session = await requestJson("/_api/auth/login/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({ username, password }),
  })
  setAuthState(session)
  return session
}

export async function logout() {
  const csrfToken = await getCsrfToken()
  await requestJson("/_api/auth/logout/", {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
    },
  })
  setAuthState({ isAuthenticated: false })
}
