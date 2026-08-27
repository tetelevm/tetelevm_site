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
  return getJson("/_api/formats/", "Форматы не найдены")
}

export function getRandomPost() {
  return getJson("/_api/random-post/", "В архиве пока нет доступных постов")
}

export function getProjectPosts(projectCode, page = 1, tagCode = "") {
  const query = new URLSearchParams({ page: String(page) })
  if (tagCode) {
    query.set("tag", tagCode)
  }
  return getJson(
    `/_api/formats/${encodeURIComponent(projectCode)}/?${query}`,
    "Формат не найден",
  )
}

export function getPost(projectCode, postNumber) {
  return getJson(
    `/_api/formats/${encodeURIComponent(projectCode)}/${encodeURIComponent(postNumber)}/`,
    "Пост не найден",
  )
}
