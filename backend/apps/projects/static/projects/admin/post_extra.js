"use strict"

function setupPostExtraFields() {
  const projectField = document.querySelector("#id_project")
  const extraFields = Array.from(
    document.querySelectorAll("[data-post-extra-types]"),
  )

  if (!projectField || extraFields.length === 0) {
    return
  }

  let postTypesByProject
  try {
    postTypesByProject = JSON.parse(
      projectField.dataset.projectPostTypes || "{}",
    )
  } catch {
    return
  }

  function updateExtraFields() {
    const selectedPostType = postTypesByProject[projectField.value]

    for (const field of extraFields) {
      let supportedPostTypes
      try {
        supportedPostTypes = JSON.parse(field.dataset.postExtraTypes || "[]")
      } catch {
        supportedPostTypes = []
      }
      const isActive = supportedPostTypes.includes(selectedPostType)
      field.disabled = !isActive
      field.required =
        isActive && field.dataset.postExtraRequired === "true"
    }
  }

  projectField.addEventListener("change", updateExtraFields)
  updateExtraFields()
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", setupPostExtraFields)
} else {
  setupPostExtraFields()
}
