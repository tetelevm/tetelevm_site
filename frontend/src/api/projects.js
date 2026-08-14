export async function getProject(link) {
  const response = await fetch(`/_api/projects/${encodeURIComponent(link)}/`, {
    credentials: "same-origin",
  })

  if (response.status === 404) {
    throw new Error("Проект не найден")
  }
  if (!response.ok) {
    throw new Error("Не удалось загрузить проект")
  }

  return response.json()
}
