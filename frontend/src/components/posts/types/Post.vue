<script setup>
import { computed } from "vue"

import MediaCarousel from "../../media/MediaCarousel.vue"
import DatedPostHeader from "../blocks/DatedPostHeader.vue"
import PlainPostText from "../blocks/PlainPostText.vue"
import PostConnections from "../blocks/PostConnections.vue"
import PostFileList from "../blocks/PostFileList.vue"
import PostImage from "../blocks/PostImage.vue"
import PostLayout from "../blocks/PostLayout.vue"

const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
})

const mediaFiles = computed(() =>
  (props.post.files ?? []).filter((file) =>
    ["photo", "video"].includes(file.mediaType),
  ),
)

const otherFiles = computed(() =>
  (props.post.files ?? []).filter(
    (file) => !["photo", "video"].includes(file.mediaType),
  ),
)
</script>

<template>
  <PostLayout>
    <DatedPostHeader :title="post.name" :date="post.date" />

    <PlainPostText :text="post.text" />

    <PostImage
      v-if="post.mainFile?.mediaType === 'photo'"
      :src="post.mainFile.link"
      :full-src="post.mainFile.linkFull"
      :alt="post.name"
      variant="stage"
      lightbox
    />

    <MediaCarousel :items="mediaFiles" :label="`Медиа: ${post.name}`" />

    <PostFileList :files="otherFiles" />

    <PostConnections
      :related-post="post.relatedPost"
      :tags="post.tags"
    />
  </PostLayout>
</template>
