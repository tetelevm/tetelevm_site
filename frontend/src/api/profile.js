export async function getProfile(language, signal) {
  const response = await fetch(`/_api/profile/${encodeURIComponent(language)}/`, {
    credentials: "same-origin",
    signal,
  })
  if (!response.ok) {
    throw new Error("Profile could not be loaded")
  }
  return response.json()
}
