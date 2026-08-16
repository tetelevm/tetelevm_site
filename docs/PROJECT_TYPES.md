# Project Types

This document describes how project item lists and individual post pages look
for each project type. Component selection architecture and API structure are
documented in `TECHNICAL.md`.

A project defines `post_list_type` for its item list and `post_type` for an
individual post. The codes are usually the same, but they can technically be
combined independently.

## General rules

- List APIs expose only the data required by their cards.
- Square cards use the small 150-by-150 thumbnail.
- A regular image preview is limited to 600 pixels on its longest side.
- The original is loaded only when a type explicitly displays the full image or
  the visitor opens a lightbox.
- Additional files follow `PostFile.order`.
- Types that show a name and overall rating share the `RatedPostGrid` and
  `RatedPostHeader` components.

## `door` — Doors

The project contains photographs of doors.

List:

- four square cards per row on wide screens;
- each photograph is center-cropped;
- `text` appears below it in the format `🚪 Country, City`;
- the grid decreases to two columns and then one on mobile devices.

Post:

- the photograph appears without square cropping;
- the `text` caption is centered below the photograph;
- the post name is not displayed.

## `photo` — Photos

List:

- four square previews per row;
- images are center-cropped;
- captions and names are not displayed;
- each card opens an individual post.

Post:

- the uncropped `mainFile.linkFull` original is displayed;
- the regular preview is used when the original link is unavailable;
- text, name, and additional files are not displayed.

## `plasticine` — Plasticine

List:

- the main photograph appears in a decorative frame;
- two cards appear per row on wide screens and one on mobile devices;
- cards have a slight rotation and straighten on hover;
- name and text are not displayed.

Post:

- the main photograph appears first;
- additional photographs follow vertically in `PostFile.order`;
- name and text are not displayed.

## `anime` — Anime

The project contains write-ups about watched anime.

List:

- four square cards per row;
- `name` appears below the main image on the left, with the overall rating on
  the right;
- the overall rating is provided by the dedicated list field `rating`, extracted
  from `extra.rating`;
- the grid decreases to two columns and then one on mobile devices.

Post:

- a large `name` appears at the top;
- `extra.original_title` appears directly below it in italics;
- a circular overall `extra.rating` sits to the right of the title block;
- three square screenshots from the first three additional files appear below;
- selecting a screenshot opens its original in a full-screen lightbox;
- the main `text` follows;
- the bottom row contains the Russian label “стоит смотреть:” (“worth
  watching:”) followed by the italicized `extra.result`.

Expected `extra` structure:

```json
{
  "original_title": "",
  "rating": null,
  "result": ""
}
```

The model and admin currently do not enforce exactly three screenshots. Missing
files produce empty slots, while additional files beyond the first three are
not displayed.

## `abandoned` — Abandoned Buildings

The project contains descriptions and ratings of abandoned buildings.

List:

- it uses the same card grid as Anime;
- each card contains a square main image, `name`, and overall `rating`.

Post:

- a large `name` appears at the top, with a circular overall `extra.rating` on
  the right;
- the main `text` follows;
- four individual rating rows appear below it;
- values from 1 to 5 are represented by the corresponding number of `🏚` emoji;
- a missing rating is represented by a dash;
- values outside the range are clamped to 1–5 for display;
- a carousel of additional files in `PostFile.order` appears below the ratings.

The carousel supports images and videos. Images open in a lightbox, while videos
use the native player controls. It provides arrows, dots, a counter, and ←/→
keyboard navigation.

Expected `extra` structure:

```json
{
  "rating": null,
  "uniqueness": null,
  "monumentality": null,
  "atmosphere": null,
  "liveliness": null
}
```

The individual rating labels shown in the current Russian interface are
“уникальность” (uniqueness), “монументальность” (monumentality), “атмосфера”
(atmosphere), and “жизненность” (liveliness).

## Placeholder types

The following types are declared by the backend and explicitly mapped to Vue
components, but their visual templates have not been designed yet:

- `post`;
- `travel`;
- `text`;
- `text_md`.

Their components currently render no content.

## JSON in Django Admin

`Post.extra` remains editable as raw JSON in a single text area. When a project
is selected, the admin prepopulates a template based on its `post_type`:

- `anime` receives `original_title`, `rating`, and `result`;
- `abandoned` receives `rating`, `uniqueness`, `monumentality`, `atmosphere`,
  and `liveliness`;
- all other types receive an empty `{}` object.

An automatically inserted template may be replaced when the project changes.
JSON that the administrator has edited manually is never overwritten.
