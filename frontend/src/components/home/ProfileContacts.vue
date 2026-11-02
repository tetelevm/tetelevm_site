<script setup>
import { computed, nextTick, onBeforeUnmount, ref, useTemplateRef } from "vue"
import { Icon } from "@iconify/vue"
import TelegramIcon from "@iconify-icons/ri/telegram-line"
import MailIcon from "@iconify-icons/ri/mail-line"
import LinkedInIcon from "@iconify-icons/ri/linkedin-box-line"
import GitHubIcon from "@iconify-icons/ri/github-line"
import InstagramIcon from "@iconify-icons/ri/instagram-line"
import LinktreeIcon from "@iconify-icons/simple-icons/linktree"
import CopyIcon from "@iconify-icons/ri/file-copy-line"
import CheckIcon from "@iconify-icons/ri/check-line"

const contactIcons = {
  telegram: TelegramIcon,
  email: MailIcon,
  linkedin: LinkedInIcon,
  github: GitHubIcon,
  channel: TelegramIcon,
  instagram: InstagramIcon,
  linktree: LinktreeIcon,
}

const props = defineProps({
  contacts: { type: Array, required: true },
  title: { type: String, default: "" },
  pending: { type: String, default: "" },
  copyLabel: { type: String, required: true },
  copiedLabel: { type: String, required: true },
  copyFailedLabel: { type: String, required: true },
})

const emailAddress = computed(() => {
  const url = props.contacts.find((contact) => contact.key === "email")?.url
  return url?.startsWith("mailto:") ? url.slice(7) : ""
})
const copied = ref(false)
const copyError = ref("")
const manualCopyInput = useTemplateRef("manualCopyInput")
let feedbackTimer

async function copyEmail() {
  window.clearTimeout(feedbackTimer)
  copied.value = false
  copyError.value = ""
  try {
    await navigator.clipboard.writeText(emailAddress.value)
    copied.value = true
    feedbackTimer = window.setTimeout(() => { copied.value = false }, 2000)
  } catch {
    copyError.value = emailAddress.value
    await nextTick()
    manualCopyInput.value?.focus()
    manualCopyInput.value?.select()
  }
}

onBeforeUnmount(() => window.clearTimeout(feedbackTimer))

const contactGroups = computed(() => [
  { id: "primary", contacts: props.contacts.filter((contact) => contact.group === "primary") },
  { id: "secondary", contacts: props.contacts.filter((contact) => contact.group === "secondary") },
])
</script>

<template>
  <section class="profile-contacts" aria-labelledby="contacts-title">
    <h2 id="contacts-title" class="profile-contacts__title">
      {{ title }}
    </h2>
    <ul
      v-for="group in contactGroups"
      :key="group.id"
      class="profile-contacts__list"
      :class="`profile-contacts__list--${group.id}`"
    >
      <li
        v-for="contact in group.contacts"
        :key="contact.key"
        :class="{
          'profile-contacts__compact': contact.compact,
          'profile-contacts__item--copyable': contact.key === 'email' && emailAddress,
        }"
      >
        <component
          :is="contact.url ? 'a' : 'div'"
          :class="contact.url ? 'profile-contacts__link' : 'profile-contacts__placeholder'"
          :href="contact.url || undefined"
          :target="contact.url ? '_blank' : undefined"
          :rel="contact.url ? 'noopener noreferrer' : undefined"
          :aria-label="contact.compact ? `${contact.label}${!contact.url ? ` — ${pending}` : ''}` : undefined"
          :title="contact.compact ? contact.label : undefined"
        >
          <Icon
            :icon="contactIcons[contact.key]"
            v-if="contact.compact"
            class="profile-contacts__icon profile-contacts__icon--compact"
            aria-hidden="true"
          />
          <template v-else>
            <span class="profile-contacts__label">
              <Icon :icon="contactIcons[contact.key]" class="profile-contacts__icon" aria-hidden="true" />
              {{ contact.label }}
            </span>
            <span class="profile-contacts__value">
              {{ contact.url ? `${contact.value || contact.label} ↗` : pending }}
            </span>
          </template>
        </component>
        <button
          v-if="contact.key === 'email' && emailAddress"
          class="profile-contacts__copy"
          type="button"
          :aria-label="copied ? copiedLabel : copyLabel"
          :title="copied ? copiedLabel : copyLabel"
          @click="copyEmail"
        >
          <Icon :icon="copied ? CheckIcon : CopyIcon" class="profile-contacts__icon" aria-hidden="true" />
        </button>
      </li>
    </ul>
    <span class="visually-hidden" role="status">{{ copied ? copiedLabel : '' }}</span>
    <div v-if="copyError" class="profile-contacts__manual-copy">
      <label for="manual-copy-email" role="alert">{{ copyFailedLabel }}</label>
      <input id="manual-copy-email" ref="manualCopyInput" :value="copyError" readonly @focus="$event.target.select()" />
    </div>
  </section>
</template>

<style scoped>
.profile-contacts {
  padding-top: 2rem;
  border-top: 1px solid var(--color-line);
}

.profile-contacts__title {
  margin: 0 0 1.1rem;
  font-family: var(--font-heading);
  font-size: 1.5rem;
  font-weight: 500;
}

.profile-contacts__list {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.75rem;
  margin: 0;
  padding: 0;
  list-style: none;
}

.profile-contacts__link,
.profile-contacts__placeholder {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  padding: 1rem;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-small);
  font-size: 0.85rem;
  text-decoration: none;
  height: 100%;
}

.profile-contacts__list + .profile-contacts__list {
  margin-top: 0.75rem;
}

.profile-contacts__list--secondary {
  grid-template-columns: repeat(3, minmax(0, 1fr)) 3rem;
}

.profile-contacts__compact {
  align-self: stretch;
}

.profile-contacts__compact .profile-contacts__link,
.profile-contacts__compact .profile-contacts__placeholder {
  width: 3rem;
  height: 100%;
  padding: 0;
  align-items: center;
  justify-content: center;
  color: var(--color-muted);
}

.profile-contacts__label {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  letter-spacing: 0.035em;
}

.profile-contacts__item--copyable {
  position: relative;
}

.profile-contacts__item--copyable .profile-contacts__label {
  padding-right: 2rem;
}

.profile-contacts__copy {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  display: grid;
  place-items: center;
  width: 2rem;
  height: 2rem;
  padding: 0;
  border: 0;
  border-radius: var(--radius-small);
  color: var(--color-muted);
  background: transparent;
  cursor: pointer;
}

.profile-contacts__copy:hover,
.profile-contacts__copy:focus-visible {
  color: var(--color-accent);
  background: var(--color-surface-raised);
}

.profile-contacts__copy:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

.profile-contacts__manual-copy {
  display: grid;
  gap: 0.5rem;
  margin-top: 0.75rem;
  color: var(--color-muted);
  font-size: 0.85rem;
}

.profile-contacts__manual-copy input {
  width: 100%;
  min-width: 0;
  padding: 0.75rem;
  border: 1px solid var(--color-accent);
  border-radius: var(--radius-small);
  color: var(--color-text);
  background: var(--color-surface);
}

.profile-contacts__icon {
  width: 1rem;
  height: 1rem;
  flex-shrink: 0;
}

.profile-contacts__icon--compact {
  width: 1.5rem;
  height: 1.5rem;
}

.profile-contacts__value {
  color: var(--color-muted);
  font-family: var(--font-caption);
  font-size: 0.9rem;
  overflow-wrap: anywhere;
}

.profile-contacts__link:hover,
.profile-contacts__link:focus-visible {
  border-color: var(--color-accent);
  outline: 2px solid var(--color-accent);
  outline-offset: 3px;
}

@media (max-width: 480px) {
  .profile-contacts__item--copyable .profile-contacts__link {
    padding-right: 3rem;
  }

  .profile-contacts__list {
    grid-template-columns: minmax(0, 1fr);
  }

  .profile-contacts__list--secondary {
    grid-template-columns: minmax(0, 1fr) 3rem;
  }

  .profile-contacts__list--secondary > li:not(.profile-contacts__compact) {
    grid-column: 1;
  }

  .profile-contacts__compact {
    grid-column: 2;
    grid-row: 3;
  }

  .profile-contacts__link,
  .profile-contacts__placeholder {
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: space-between;
  }
}
</style>
