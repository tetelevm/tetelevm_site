# Format Types

Formats independently choose a list type (`post_list_type`) and detail type
(`post_type`). Their explicit Vue mappings live in `config/postTypes.js`.

## Shared presentation

- Square card grids have three columns on desktop, reducing to two and one.
  Variants are `photo_card` (image only), `label_photo_card` (image and label),
  and `rated_photo_card` (image, label, and circular rating). One frame encloses
  the whole card. Images are center-cropped 150px thumbnails.
- `row_card` uses a full-width row with a 100px media slot, a label/optional
  rating, and an optional date below. An empty media slot keeps labels aligned.
- The main file supplies list previews; otherwise the first ordered additional
  file is used. Non-images leave the image slot empty.
- Labels prefer a trimmed name, a normalized text excerpt (up to 90 characters),
  then unique-file counts; empty posts use `🌀`. Hidden labels remain accessible.
- Detail headers show an optional name and date (`YYYY.MM.DD`). Anime adds its
  original title/year and rating; abandoned buildings add their rating.
- Detail images use originals without cropping. Carousels preserve image/video
  proportions, stop at either end, and do not capture browser arrow shortcuts.
  Their current height stays in place until the next image loads. Photos open
  in the shared lightbox. Additional files retain their configured order.
- The shared footer contains visible related posts as row cards, linked tags,
  and adjacent-post links when available. Forward precedes back, also on mobile;
  framed links use up to 80 characters of the label and wrap long strings.
- Headings use Sofia Sans, body copy the interface sans-serif stack, and dates,
  captions, and ratings IBM Plex Mono. Layouts remain usable on mobile.

## Detail types

| Code | Usual list | Detail body |
| --- | --- | --- |
| `door` | Labeled photo cards | Uncropped main photo, then centered text caption (usually `🚪 Country, City`). |
| `photo` | Image-only cards | Main photo only; text and additional files are omitted. |
| `plasticine` | Labeled photo cards | Main photo, divider, then additional photos in a carousel; no text. |
| `anime` | Rated photo cards | Original title/year and rating in header, first three additional screenshots, Markdown text, then “стоит смотреть:” and italic recommendation. |
| `abandoned` | Rated photo cards | Linked coordinates, text, four individual ratings, then additional image/video carousel. |
| `text` | Rows | Plain text with line breaks, then main/additional media in a carousel. |
| `text_md` | Rows | Markdown body, including embedded media; attachments are not appended automatically. |
| `travel` | Rows | Carousel of additional photos only, then plain text or Markdown when `extra.md` is true. |
| `post` | Rows | Plain text or optional Markdown, main image, media carousel, then remaining download links. |

Anime card labels are limited to three visible lines, with full accessible/hover
text. Its screenshots open in the lightbox; extra screenshots after the first
three are omitted, and missing ones leave empty slots.

Abandoned-building coordinates appear below the title only when latitude,
longitude, and a safe external map link are all present. Individual ratings are
“уникальность”, “монументальность”, “атмосфера”, and “жизненность”: one to five
`🏚` symbols, a dash if absent, and display values clamped to that range.

## Markdown and media

Markdown is always enabled for `anime` and `text_md`, and optional for `post`
and `travel`. Raw HTML is disabled. The shared renderer styles ordinary Markdown
blocks and `::: spoiler [title]` containers, collapsed until opened.
Format descriptions use the same renderer.

Markdown images open in the lightbox. Image syntax also renders recognized
video/audio URLs as native players and other files as download links; non-empty
image labels become visible media captions. Structured attachments select the
player from their stored media type. Plain text preserves line breaks, and
long uninterrupted strings wrap within the content width.

## Type-specific metadata

Admin exposes validated fields for `Post.extra`, enabling those of the selected
type. Changing types removes known irrelevant keys while retaining unknown data.

| Type | Fields |
| --- | --- |
| `post`, `travel` | Optional boolean `md`; plain text by default. |
| `anime` | Required `original_title`, integer `rating` (1–10), and one-line `result`; optional integer `year`. |
| `abandoned` | Overall float `rating` (1–5); `location.latitude`/`longitude` as floats and `location.link`; integer `uniqueness`, `monumentality`, `atmosphere`, `liveliness` (1–5). |
| Other types | No type-specific fields. |
