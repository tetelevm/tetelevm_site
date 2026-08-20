export function formatDate(value) {
  if (typeof value !== "string") {
    return ""
  }

  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value)
  return match ? `${match[1]}.${match[2]}.${match[3]}` : value
}
