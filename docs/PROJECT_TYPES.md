# Project Types

This document describes how project item lists and individual post pages look
for each project type. Component selection architecture and API structure are
documented in `TECHNICAL.md`.

A project defines `post_list_type` for its item list and `post_type` for an
individual post. List types describe reusable card presentations and can be
combined independently with detail post types. The supported list codes are
`row_card`, `photo_card`, `label_photo_card`, and `rated_photo_card`.

## General rules

- List APIs expose only the data required by their cards.
- Square cards use the small 150-by-150 thumbnail.
- A regular image preview is limited to 600 pixels on its longest side.
- The original is loaded only when a type explicitly displays the full image or
  the visitor opens a lightbox.
- Additional files follow `PostFile.order`.
- Media carousels preserve the active image or video's aspect ratio instead of
  cropping it into a fixed frame. Their height changes when visitors switch
  between portrait and landscape items.
- Carousel navigation is bounded: the previous control is disabled on the
  first item and the next control on the last. Carousels do not bind keyboard
  arrow keys, leaving browser shortcuts such as `Alt+←` and `Alt+→` intact.
- The active carousel image loads eagerly. During a slide change, the stage
  retains the current item's aspect ratio until the next item has loaded, then
  resizes once to the new ratio instead of collapsing in between.
- Framed standalone images also preserve their natural aspect ratio; the frame
  follows the image instead of imposing a fixed shape.
- Plain post body text uses the shared sans-serif face at `1.2rem`; long
  uninterrupted strings wrap instead of extending beyond the post width.
- Headers that contain both a name and date place the name on the left and the
  date on the right.
- All dates in the public frontend are displayed as `YYYY.MM.DD`.
- Card lists use the shared `PostCardList`: one outer frame encloses the
  square-cropped image and an optional caption containing a label and rating,
  so they read as a single card. Image-only cards omit the caption section.
- Row lists use the shared `PostRowList` with a 100-pixel media slot, label, and
  optional date positioned near the bottom edge of the row.
- Shared list-type adapters decide which post data becomes the image, label,
  rating, and date; `PostCardList` and `PostRowList` only render those values.
- Every list item receives the shared post label. It prefers a trimmed `name`,
  then a whitespace-normalized `text` excerpt of at most 90 characters, then
  unique-file counts such as `📷 3 · 🎬 1 · 🎵 1 · 📎 2`; a completely empty
  post uses `🌀`. Type-specific lists may omit the visible caption when their
  presentation is intentionally image-only, while still using the label for
  accessible image text.
- Detail types that show a name and overall rating share `RatedPostHeader`.
- Detail pages compose the shared `PostLayout`, `PostTitle`, `PlainPostText`,
  `PostImage`, media, and connection blocks where applicable. Type components
  retain only their data selection and genuinely type-specific markup.
- Every detail page ends with text links to the nearest lower-numbered and
  higher-numbered posts in the same project. Each link contains an arrow, the
  project name, post number, and up to 80 characters of the shared post label.
  The higher-numbered forward link is on the left and precedes the
  lower-numbered back link, including in the single-column mobile layout.
  The whole link is framed, and uninterrupted text wraps within its half of the
  navigation row instead of overlapping the other link.
- Every detail type ends with one shared post-footer block between its
  type-specific body and the site footer. It contains visible related posts in
  the row-card presentation, all tag labels, and neighboring-post navigation,
  omitting whichever sections have no data.

## `door` — Doors

The project contains photographs of doors.

List:

- three square cards per row on wide screens;
- each photograph is center-cropped;
- the shared label appears below it; for the usual nameless door post this is
  its `text` in the format `🚪 Country, City`;
- the grid decreases to two columns and then one on mobile devices.

Post:

- the photograph appears without square cropping;
- the `text` caption is centered below the photograph;
- the post name is not displayed.

## `photo` — Photos

List:

- three square previews per row;
- images are center-cropped;
- no caption is displayed; the card contains only the image;
- each card opens an individual post.

Post:

- the uncropped `mainFile.linkFull` original is displayed;
- the regular preview is used when the original link is unavailable;
- text, name, and additional files are not displayed.

## `plasticine` — Plasticine

List:

- it uses the same labeled photo-card presentation as `door`;
- the square thumbnail of `mainFile` appears center-cropped;
- three cards appear per row on wide screens, decreasing responsively;
- the shared post label appears below the image; the date is not displayed.

Post:

- the optional post date appears on the right in the shared dated header;
- the full main photograph appears first;
- a simple horizontal divider separates it from the additional photographs;
- additional photographs appear in the shared adaptive carousel in
  `PostFile.order`;
- photographs open their originals in the shared full-screen lightbox;
- name and text are not displayed.

## `anime` — Anime

The project contains write-ups about watched anime.

List:

- three square cards per row;
- the shared label appears below the main image on the left, with the overall
  rating on the right;
- the overall rating is provided by the dedicated list field `rating`, extracted
  from `extra.rating`;
- the grid decreases to two columns and then one on mobile devices.

Post:

- a moderately sized `name` appears at the top, followed by a divider with
  spacing between the title block and the line;
- optional `extra.season` appears in italics immediately after `name` on the
  same title line; when both no longer fit, the season moves separately rather
  than taking the title's final word with it;
- `extra.original_title` appears directly below it in italics;
- a circular overall `extra.rating` sits to the right of the title block;
- three square screenshots from the first three additional files appear below;
- selecting a screenshot opens its original in a full-screen lightbox;
- the main `text` follows;
- the bottom row contains the Russian label “стоит смотреть:” (“worth
  watching:”) in slightly smaller uppercase text, followed by the italicized
  `extra.result`, without its own top divider.

Expected `extra` structure:

```json
{
  "original_title": "Sousou no Frieren",
  "season": "Сезон 2",
  "rating": 9,
  "result": "точно да"
}
```

`original_title` and the one-line `result` are required strings, `season` is an
optional string, and `rating` is an integer from 1 through 10 inclusive.

The model and admin currently do not enforce exactly three screenshots. Missing
files produce empty slots, while additional files beyond the first three are
not displayed.

## `abandoned` — Abandoned Buildings

The project contains descriptions and ratings of abandoned buildings.

List:

- it uses the same card grid as Anime;
- each card contains a square main image, the shared label, and overall `rating`.

Post:

- a large `name` appears at the top, with a circular overall `extra.rating` on
  the right;
- when `extra.location.latitude`, `longitude`, and `link` are all present, the
  coordinates appear directly below the title as a working external link such
  as `12.345, 34.567`;
- the main `text` follows;
- four individual rating rows appear below it;
- values from 1 to 5 are represented by the corresponding number of `🏚` emoji;
- a missing rating is represented by a dash;
- values outside the range are clamped to 1–5 for display;
- a carousel of additional files in `PostFile.order` appears below the ratings.

The carousel supports images and videos. Images open in a lightbox, while videos
use the native player controls. It provides bounded on-screen arrows, dots, and
a counter without keyboard-arrow navigation.

Expected `extra` structure:

```json
{
  "rating": 4.5,
  "location": {
    "latitude": 41.6880746,
    "longitude": 44.8216462,
    "link": "https://www.openstreetmap.org/"
  },
  "uniqueness": 5,
  "monumentality": 3,
  "atmosphere": 4,
  "liveliness": 2
}
```

The overall `rating` is a float from 1 through 5 inclusive. Coordinates are
floats and the location link is a string. The four individual ratings are
integers from 1 through 5 inclusive.

The individual rating labels shown in the current Russian interface are
“уникальность” (uniqueness), “монументальность” (monumentality), “атмосфера”
(atmosphere), and “жизненность” (liveliness).

## `text` — Texts

List:

- posts form a vertical list rather than an image grid;
- each post is a full-width row with a fixed 100-pixel media slot on the left;
- an image `mainFile` fills that slot with its square thumbnail;
- the slot remains empty for a missing or non-image `mainFile`, keeping all
  names aligned; there is no media-slot divider when no image is present;
- the shared label appears after the media slot;
- the optional model field `date` appears on the right.

Post:

- `name` appears in a larger type size at the top on the left;
- the optional `date` appears on the right;
- the plain `text` follows with its line breaks preserved;
- when `mainFile` or additional files exist, they appear after the text in the
  shared image-and-video media carousel.

## `text_md` — Markdown Texts

The list is identical to `text` and uses the shared `PostRowList` component:

- each item is a full-width row with a fixed 100-pixel thumbnail slot;
- the shared label follows the slot and the optional `date` appears on the
  right;
- the thumbnail slot remains empty when there is no image `mainFile`.

Post:

- the header matches `text`, with `name` on the left and optional `date` on the
  right;
- `text` is rendered as Markdown;
- blocks written as `::: spoiler Optional title` through a closing `:::` are
  collapsed by default and expand when their summary is activated;
- headings, paragraphs, lists, links, blockquotes, code blocks, tables, images,
  and Markdown line breaks are styled for the site;
- raw HTML embedded in Markdown is disabled and displayed as text.

Project descriptions use the same safe Markdown renderer and support the same
click-to-expand `::: spoiler [title]` blocks.

## `travel` — Travel

The list is identical to `text` and `text_md` and uses `PostRowList`:

- each item is a full-width row with a fixed 100-pixel thumbnail slot;
- an image `mainFile` appears in that slot;
- the shared label follows the thumbnail and optional `date` appears on the
  right.

Post:

- a large `name` appears on the top left and optional `date` on the right;
- an image carousel follows, containing only image additional files in
  `PostFile.order`; `mainFile` is not duplicated in the post carousel;
- selecting a photograph opens its original in the shared lightbox;
- the plain `text` appears below the carousel with line breaks preserved;

## `post` — General Posts

List:

- posts use the same full-width row structure as the text lists;
- an image `mainFile` appears in the fixed 100-pixel thumbnail slot; the slot is
  empty when `mainFile` is absent or is not an image;
- the row uses the shared post label;
- optional `date` appears on the right.

Post:

- the shared dated header shows `name` on the left and optional `date` on the
  right;
- `text` appears below the header as plain text with line breaks preserved by
  default;
- when `extra.md` is exactly `true`, `text` uses the shared Markdown renderer
  instead, with raw embedded HTML disabled;
- an image `mainFile`, when present, appears below the text in an
  aspect-ratio-preserving frame and opens its original in the shared lightbox;
- a carousel follows with additional files whose `mediaType` is `photo` or
  `video`;
- remaining additional files appear as a vertical list of links using their
  original upload names;

Expected `extra` structure:

```json
{
  "md": false
}
```

## Type-specific fields in Django Admin

`Post.extra` is not shown as raw JSON. The admin displays all individual typed
fields together in one block, enabling the subset selected by the project's
`post_type`:

- `post` shows the optional `md` checkbox;
- `anime` shows `original_title`, optional `season`, integer `rating` from 1 to
  10, and the one-line `result`;
- `abandoned` shows float `rating` from 1 to 5, float location coordinates, a
  string location link, and four integer ratings from 1 to 5;
- all other types leave every `extra` control disabled.

Changing the selected project switches which fields are enabled and required;
the complete field set remains visible. Saving removes known metadata belonging
to other post types while retaining unknown JSON keys.
