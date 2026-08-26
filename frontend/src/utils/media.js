const MEDIA_EXTENSIONS = {
  photo: new Set(["avif", "gif", "jpeg", "jpg", "png", "webp"]),
  video: new Set(["m4v", "mov", "mp4", "ogv", "webm"]),
  audio: new Set(["aac", "flac", "m4a", "mp3", "ogg", "opus", "wav"]),
}

export function mediaTypeFromUrl(value = "") {
  const path = value.split(/[?#]/, 1)[0]
  const extension = path.includes(".")
    ? path.slice(path.lastIndexOf(".") + 1).toLowerCase()
    : ""

  return Object.entries(MEDIA_EXTENSIONS).find(([, extensions]) =>
    extensions.has(extension),
  )?.[0] ?? "other"
}

export function resolvedMediaType(mediaType, source) {
  return ["photo", "video", "audio", "other"].includes(mediaType)
    ? mediaType
    : mediaTypeFromUrl(source)
}
