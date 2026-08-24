document.addEventListener("DOMContentLoaded", () => {
  const pasteArea = document.querySelector(".clipboard-upload")
  const fileInput = document.querySelector("#id_content")

  if (!pasteArea || !fileInput || typeof DataTransfer === "undefined") {
    return
  }

  function extensionFor(file) {
    const extensions = {
      "image/avif": "avif",
      "image/gif": "gif",
      "image/jpeg": "jpg",
      "image/png": "png",
      "image/webp": "webp",
    }
    return extensions[file.type] || "png"
  }

  function clipboardFilename(file) {
    const timestamp = new Date().toISOString().replace(/[-:]/g, "").slice(0, 15)
    return `clipboard-${timestamp}.${extensionFor(file)}`
  }

  pasteArea.addEventListener("paste", (event) => {
    const image = [...(event.clipboardData?.items ?? [])]
      .find((item) => item.kind === "file" && item.type.startsWith("image/"))
      ?.getAsFile()

    if (!image) {
      pasteArea.querySelector(".clipboard-upload__status").textContent =
        pasteArea.dataset.noImageText
      return
    }

    event.preventDefault()
    const files = new DataTransfer()
    files.items.add(
      new File([image], clipboardFilename(image), {
        type: image.type,
        lastModified: image.lastModified,
      }),
    )
    fileInput.files = files.files
    pasteArea.querySelector(".clipboard-upload__status").textContent =
      `${pasteArea.dataset.addedText} ${files.files[0].name}`
  })
})
