<script setup>
import { computed, ref, watch } from "vue"
import LanguageSwitch from "../components/common/LanguageSwitch.vue"
import MainLayout from "../components/layout/MainLayout.vue"
import ProfileIntro from "../components/home/ProfileIntro.vue"
import ProfileContacts from "../components/home/ProfileContacts.vue"
import ProfileResume from "../components/home/ProfileResume.vue"
import { contactLayout } from "../config/profile.js"
import { getProfile } from "../api/profile.js"
import PageStatus from "../components/common/PageStatus.vue"
import { setPageMeta } from "../utils/pageMeta.js"

const language = ref("ru")
const profile = ref(null)
const loading = ref(false)
const failed = ref(false)
const contacts = computed(() => profile.value
  ? contactLayout.map((item) => ({ ...item, ...profile.value.contacts[item.key] }))
  : [])

watch(language, async (value, _oldValue, onCleanup) => {
  const controller = new AbortController()
  onCleanup(() => controller.abort())
  loading.value = true
  failed.value = false
  profile.value = null
  try {
    const data = await getProfile(value, controller.signal)
    if (!controller.signal.aborted) profile.value = data
  } catch (error) {
    if (!controller.signal.aborted) failed.value = true
  } finally {
    if (!controller.signal.aborted) loading.value = false
  }
}, { immediate: true })

const pageDescription = {
  ru: "Личный сайт и архив форматов tetelevm.",
  en: "The personal website and format archive of tetelevm.",
}

watch(
  language,
  (value) => {
    setPageMeta({
      title: "tetelevm",
      socialTitle: "tetelevm - Main",
      description: pageDescription[value],
      path: "/",
      language: value,
    })
  },
  { immediate: true },
)
</script>

<template>
  <MainLayout active-page="home" :language="language">
    <template #header-action>
      <LanguageSwitch v-model="language" />
    </template>

    <PageStatus
      :loading="loading"
      :loading-text="language === 'ru' ? 'Загрузка…' : 'Loading…'"
      :error="failed ? (language === 'ru' ? 'Не удалось загрузить визитку. Попробуйте обновить страницу.' : 'Could not load the profile. Please refresh the page.') : ''"
    />
    <div v-if="profile" class="home-profile">
      <ProfileIntro
        :name="profile.name"
        :role="profile.role"
        :about="profile.about"
        :looking-for-work="profile.lookingForWork"
        :photo-url="profile.photoUrl"
        :availability-text="profile.availabilityText"
        :photo-placeholder="profile.photoPlaceholder"
      />
      <ProfileContacts :contacts="contacts" :title="profile.contactsTitle" :pending="profile.contactPending" />
      <ProfileResume
        :url="profile.resumeUrl"
        :preview-url="profile.resumePreviewUrl"
        :title="profile.resumeTitle"
        :description="profile.resumeDescription"
        :pending="profile.resumePending"
      />
    </div>

    <template #before-footer>
      <p v-if="profile" class="home-credit">
        {{ profile.footerCredit }}
      </p>
    </template>
  </MainLayout>
</template>

<style scoped>
.home-profile {
  display: grid;
  gap: clamp(2rem, 5vw, 3rem);
}

.home-credit {
  margin: 0;
  color: var(--color-muted);
  font-size: 0.72rem;
  line-height: 1.5;
  text-align: right;
}
</style>
