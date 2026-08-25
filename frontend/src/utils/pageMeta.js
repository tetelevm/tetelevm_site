const META_ATTRIBUTE = "data-page-meta"
const ARCHIVE_DESCRIPTION = "Projects archive: texts, photos and other"

function setMetaTag(attribute, key, content) {
  let element = document.head.querySelector(
    `meta[${attribute}="${key}"][${META_ATTRIBUTE}]`,
  )
  if (!element) {
    element = document.createElement("meta")
    element.setAttribute(attribute, key)
    element.setAttribute(META_ATTRIBUTE, "")
    document.head.append(element)
  }
  element.setAttribute("content", content)
}

function setCanonical(url) {
  let element = document.head.querySelector(`link[rel="canonical"][${META_ATTRIBUTE}]`)
  if (!element) {
    element = document.createElement("link")
    element.setAttribute("rel", "canonical")
    element.setAttribute(META_ATTRIBUTE, "")
    document.head.append(element)
  }
  element.setAttribute("href", url)
}

function removeMetaTag(attribute, key) {
  document.head
    .querySelector(`meta[${attribute}="${key}"][${META_ATTRIBUTE}]`)
    ?.remove()
}

function absoluteUrl(path) {
  return new URL(path, window.location.origin).href
}

export function fileCountDescription(post) {
  const files = [post?.mainFile, ...(post?.files ?? [])].filter(Boolean)
  const uniqueFiles = [...new Map(files.map((file) => [file.id ?? file.link, file])).values()]
  const icons = {
    photo: "📷",
    video: "🎬",
    audio: "🎵",
    other: "📎",
  }
  const counts = Object.fromEntries(Object.keys(icons).map((type) => [type, 0]))
  for (const file of uniqueFiles) {
    if (file.mediaType in counts) {
      counts[file.mediaType] += 1
    }
  }
  return Object.entries(icons)
    .filter(([type]) => counts[type] > 0)
    .map(([type, icon]) => `${counts[type]} ${icon}`)
    .join(" · ")
}

export function textDescription(text, limit = 160) {
  const normalized = (text ?? "").replace(/\s+/g, " ").trim()
  if (normalized.length <= limit) {
    return normalized
  }
  return `${normalized.slice(0, limit - 1).trimEnd()}…`
}

export function setPageMeta({
  title,
  socialTitle,
  description = "",
  image = "/favicon.ico",
  path = window.location.pathname,
  type = "website",
  language = "ru",
  noindex = false,
  canonical = true,
}) {
  const canonicalUrl = absoluteUrl(path)
  const imageUrl = absoluteUrl(image)

  document.documentElement.lang = language
  document.title = title
  if (canonical) {
    setCanonical(canonicalUrl)
  } else {
    document.head
      .querySelector(`link[rel="canonical"][${META_ATTRIBUTE}]`)
      ?.remove()
  }
  setMetaTag("property", "og:type", type)
  setMetaTag("property", "og:title", socialTitle)
  if (canonical) {
    setMetaTag("property", "og:url", canonicalUrl)
  } else {
    removeMetaTag("property", "og:url")
  }
  setMetaTag("property", "og:image", imageUrl)
  setMetaTag("property", "og:locale", language === "en" ? "en_US" : "ru_RU")
  setMetaTag(
    "name",
    "twitter:card",
    image === "/favicon.ico" ? "summary" : "summary_large_image",
  )
  setMetaTag("name", "twitter:title", socialTitle)
  setMetaTag("name", "twitter:image", imageUrl)
  if (noindex) {
    setMetaTag("name", "robots", "noindex")
  } else {
    removeMetaTag("name", "robots")
  }

  if (description) {
    setMetaTag("name", "description", description)
    setMetaTag("property", "og:description", description)
    setMetaTag("name", "twitter:description", description)
  } else {
    removeMetaTag("name", "description")
    removeMetaTag("property", "og:description")
    removeMetaTag("name", "twitter:description")
  }
}

export function setDefaultPageMeta(routeName) {
  if (routeName === "home") {
    setPageMeta({title: "tetelevm", socialTitle: "tetelevm - Main", path: "/"})
    return
  }
  if (routeName === "projects") {
    setPageMeta({
      title: "Project archive",
      socialTitle: "tetelevm - Archive",
      description: ARCHIVE_DESCRIPTION,
      path: "/archive/",
    })
    return
  }
  if (routeName === "login") {
    setPageMeta({
      title: "Login",
      socialTitle: "tetelevm - Login",
      path: "/login/",
      noindex: true,
    })
    return
  }
  if (routeName === "random-post") {
    setPageMeta({
      title: "Random post",
      socialTitle: "tetelevm - Random post",
      noindex: true,
      canonical: false,
    })
    return
  }
  setPageMeta({
    title: import.meta.env.PROD ? "tetelevm" : "tetelevm.dev",
    socialTitle: "tetelevm",
  })
}
