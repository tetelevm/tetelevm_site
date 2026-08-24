async function getJson(path, notFoundMessage) {
  const response = await fetch(path, {
    credentials: "same-origin",
  })

  if (response.status === 404) {
    const error = new Error(notFoundMessage)
    error.status = response.status
    throw error
  }
  if (!response.ok) {
    throw new Error("Не удалось загрузить данные")
  }

  return response.json()
}

export function getProjects() {
  return getJson("/_api/projects/", "Архив не найден")
}

export function getRandomPost() {
  return getJson("/_api/random-post/", "В архиве пока нет доступных постов")
}

export function getProjectPosts(projectCode, page = 1) {
  return getJson(
    `/_api/projects/${encodeURIComponent(projectCode)}/?page=${encodeURIComponent(page)}`,
    "Проект не найден",
  )
}

export function getPost(projectCode, postNumber) {
  return getJson(
    `/_api/projects/${encodeURIComponent(projectCode)}/${encodeURIComponent(postNumber)}/`,
    "Пост не найден",
  )
}
