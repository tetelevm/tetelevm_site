"use strict"

function setupProjectExtraTemplate() {
  const projectField = document.querySelector("#id_project")
  const extraField = document.querySelector("#id_extra")

  if (!projectField || !extraField) {
    return
  }

  let templates
  try {
    templates = JSON.parse(extraField.dataset.projectExtraTemplates || "{}")
  } catch {
    return
  }

  let lastApplied = null

  function formattedTemplate() {
    const template = templates[projectField.value] ?? {}
    return JSON.stringify(template, null, 2)
  }

  function isEmptyJson(value) {
    const normalized = value.trim()
    return normalized === "" || normalized === "{}" || normalized === "null"
  }

  function applyTemplate() {
    const currentValue = extraField.value.trim()
    if (!isEmptyJson(currentValue) && currentValue !== lastApplied) {
      return
    }

    const nextTemplate = formattedTemplate()
    extraField.value = nextTemplate
    lastApplied = nextTemplate
  }

  const selectedTemplate = formattedTemplate()
  if (extraField.value.trim() === selectedTemplate) {
    lastApplied = selectedTemplate
  }

  projectField.addEventListener("change", applyTemplate)
  applyTemplate()
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", setupProjectExtraTemplate)
} else {
  setupProjectExtraTemplate()
}
