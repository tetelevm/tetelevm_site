<script setup>
import { computed } from "vue"

const props = defineProps({
  contacts: { type: Array, required: true },
  title: { type: String, default: "" },
  pending: { type: String, default: "" },
})

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
        :class="{ 'profile-contacts__compact': contact.compact }"
      >
        <component
          :is="contact.url ? 'a' : 'div'"
          :class="contact.url ? 'profile-contacts__link' : 'profile-contacts__placeholder'"
          :href="contact.url || undefined"
          :aria-label="contact.compact ? `${contact.label}${!contact.url ? ` — ${pending}` : ''}` : undefined"
          :title="contact.compact ? contact.label : undefined"
        >
          <svg v-if="contact.compact" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M12 3v13M7 5l10 10M17 5 7 15M4 10h16M10 17v4h4v-4" />
          </svg>
          <template v-else>
            <span>{{ contact.label }}</span>
            <span class="profile-contacts__value">
              {{ contact.url ? `${contact.value || contact.label} ↗` : pending }}
            </span>
          </template>
        </component>
      </li>
    </ul>
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
  gap: 0.65rem;
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

.profile-contacts__value {
  color: var(--color-muted);
  font-family: var(--font-caption);
  font-size: 0.72rem;
  overflow-wrap: anywhere;
}

.profile-contacts__link:hover,
.profile-contacts__link:focus-visible {
  border-color: var(--color-accent);
  outline: 2px solid var(--color-accent);
  outline-offset: 3px;
}

@media (max-width: 480px) {
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
