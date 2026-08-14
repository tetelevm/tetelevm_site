async function getJson(path, notFoundMessage) {
  const response = await fetch(path, {
    credentials: "same-origin",
  })

  if (response.status === 404) {
    throw new Error(notFoundMessage)
  }
  if (!response.ok) {
    throw new Error("Не удалось загрузить данные")
  }

  return response.json()
}

export function getProjects() {
  return getJson("/_api/projects/", "Проекты не найдены")
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
