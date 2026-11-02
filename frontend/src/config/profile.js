// Layout and interface copy stay on the frontend; editable content comes from the API.
export const contactLayout = [
  { key: "telegram", group: "primary" },
  { key: "email", group: "primary" },
  { key: "linkedin", group: "primary" },
  { key: "github", group: "secondary" },
  { key: "channel", group: "secondary" },
  { key: "instagram", group: "secondary" },
  { key: "linktree", group: "secondary", compact: true },
]

export const profileText = {
  ru: {
    availabilityText: "Ищу работу, пишите!",
    photoPlaceholder: "Здесь будет фото",
    contactsTitle: "Контакты",
    contactPending: "Скоро",
    copyEmail: "Скопировать адрес почты",
    emailCopied: "Адрес скопирован",
    emailCopyFailed: "Автоматическое копирование недоступно. Скопируйте выделенный адрес:",
    resumeTitle: "Резюме",
    resumeDescription: "Всё подробное - внутри",
    resumePending: "Файл скоро появится здесь",
    footerCredit: "Спасибо роботам-муравьишкам 🐜",
    contactLabels: {
      telegram: "Telegram", email: "Email", linkedin: "LinkedIn", github: "GitHub",
      channel: "Путешествия", instagram: "Instagram", linktree: "Linktree",
    },
  },
  en: {
    availabilityText: "Open to work, get in touch!",
    photoPlaceholder: "Photo coming soon",
    contactsTitle: "Contacts",
    contactPending: "Coming soon",
    copyEmail: "Copy email address",
    emailCopied: "Address copied",
    emailCopyFailed: "Automatic copying is unavailable. Copy the selected address:",
    resumeTitle: "Resume",
    resumeDescription: "All the details are inside",
    resumePending: "The file will be here soon",
    footerCredit: "Thanks to the ant robots 🐜",
    contactLabels: {
      telegram: "Telegram", email: "Email", linkedin: "LinkedIn", github: "GitHub",
      channel: "Travel channel", instagram: "Instagram", linktree: "Linktree",
    },
  },
}
