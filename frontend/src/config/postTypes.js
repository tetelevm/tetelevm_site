import LabelPhotoCard from "../components/posts/list-types/LabelPhotoCard.vue"
import PhotoCard from "../components/posts/list-types/PhotoCard.vue"
import RatedPhotoCard from "../components/posts/list-types/RatedPhotoCard.vue"
import RowCard from "../components/posts/list-types/RowCard.vue"
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
  post: RowCard,
  photo: PhotoCard,
  travel: RowCard,
  text: RowCard,
  text_md: RowCard,
  door: LabelPhotoCard,
  anime: RatedPhotoCard,
  plasticine: LabelPhotoCard,
  abandoned: RatedPhotoCard,
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

export const DEFAULT_POST_LIST_COMPONENT = RowCard
export const DEFAULT_POST_COMPONENT = GeneralPost
