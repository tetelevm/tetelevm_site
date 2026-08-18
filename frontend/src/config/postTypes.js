import AbandonedList from "../components/posts/list-types/Abandoned.vue"
import AnimeList from "../components/posts/list-types/Anime.vue"
import DoorList from "../components/posts/list-types/Door.vue"
import PhotoList from "../components/posts/list-types/Photo.vue"
import PlasticineList from "../components/posts/list-types/Plasticine.vue"
import GeneralPostList from "../components/posts/list-types/Post.vue"
import TextList from "../components/posts/list-types/Text.vue"
import TextMdList from "../components/posts/list-types/TextMd.vue"
import TravelList from "../components/posts/list-types/Travel.vue"
import AbandonedPost from "../components/posts/types/Abandoned.vue"
import AnimePost from "../components/posts/types/Anime.vue"
import DoorPost from "../components/posts/types/Door.vue"
import PhotoPost from "../components/posts/types/Photo.vue"
import PlasticinePost from "../components/posts/types/Plasticine.vue"
import GeneralPost from "../components/posts/types/Post.vue"
import TextPost from "../components/posts/types/Text.vue"
import TextMdPost from "../components/posts/types/TextMd.vue"
import TravelPost from "../components/posts/types/Travel.vue"

export const POST_LIST_COMPONENTS = {
  post: GeneralPostList,
  photo: PhotoList,
  travel: TravelList,
  text: TextList,
  text_md: TextMdList,
  door: DoorList,
  anime: AnimeList,
  plasticine: PlasticineList,
  abandoned: AbandonedList,
}

export const POST_COMPONENTS = {
  post: GeneralPost,
  photo: PhotoPost,
  travel: TravelPost,
  text: TextPost,
  text_md: TextMdPost,
  door: DoorPost,
  anime: AnimePost,
  plasticine: PlasticinePost,
  abandoned: AbandonedPost,
}

export const DEFAULT_POST_LIST_COMPONENT = GeneralPostList
export const DEFAULT_POST_COMPONENT = GeneralPost
