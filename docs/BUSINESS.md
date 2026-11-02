# Product Requirements

## Purpose and access

A personal website with an author presentation and an archive of texts,
photographs, and other material. Visitors read and view content; there is no
public registration, commenting, or visitor publishing.

| Role | Capabilities |
| --- | --- |
| Anonymous | View the home page, public formats and published posts; open guest login. |
| Guest | Also view private formats and their published posts; sign out. Access is read-only. |
| Administrator | Manage formats, posts, files, and the presentation through Django Admin. |

Visibility belongs to a format and is inherited by its posts. Private content
must stay hidden from anonymous visitors in lists, direct links, metadata,
random selection, and related-post links. Drafts are an authoring exception:
only staff can open them directly; they never appear in public collections.

## Home page

The home page presents Михаил Тетелев as a Python developer with a square photo,
a short introduction, and an optional “Ищу работу, пишите!” badge. Long text
wraps around the photo on desktop; the photo sits above it on mobile.

Contacts have two rows: Telegram, email, LinkedIn; then GitHub, a Telegram
channel, Instagram, and a narrow icon-only Linktree card of the same height.
The résumé heading and left tile open the PDF in a new tab. The tile shows a
manually uploaded preview without cropping, or “PDF” when no preview is chosen.
Missing files or contacts show placeholders. A small gray ant-robot credit
appears on the right before the footer.

The owner manually creates separate Russian and English “Визитки” records and
edits their copy, captions, contacts, status, photo, PDF, and preview through
ordinary administrative fields. Photo/preview selections must be images and
the résumé a PDF. Changes appear on the next page load; layout stays fixed.
The `ru/en` switch changes the presentation, navigation, and footer for the
current visit without persisting the choice.

## Archive

`/archive/` lists independent themed formats rather than a mixed post feed.
Each format has a name, Markdown description, cover, visibility, display order,
lifecycle status, and presentation types. Descriptions support collapsible
spoilers. Detailed list and post presentation belongs in [PROJECT_TYPES.md](PROJECT_TYPES.md).

Cards show post counts. Open formats have no status badge; paused formats show
“на паузе” in warm yellow-orange, closed formats “завершён” in red. Private
formats use a gray cover lock and are not dimmed. Format pages repeat the
lifecycle status beside the count.

Published posts have positive numbers; draft numbers are zero or negative.
Drafts are excluded from counts, lists, tag filtering, random selection, and
related/adjacent navigation for every role. Staff can open drafts directly;
the page is excluded from indexing and has no adjacent-post navigation.

Posts can have ordered files, tags, and symmetric links to other posts.
A tag opens the current format filtered by its code, preserving the filter
through pagination. The active filter shows its name, or the code if unknown.
Related posts follow the same visibility rules as the rest of the archive.
Adjacent links find the nearest published numbers within the same format,
skipping gaps; forward appears before back.

`/archive/random/` opens a random visible published post tagged `star`.
Unknown URLs and missing content return a real localized 404 page with a
language switch and a link to random visible material.

## Login and authoring

The visitor login matches the site design and creates a standard session.
The header logo reveals login/logout after three quick activations; `/login/`
remains directly accessible. Staff also have a link to Django Admin.

The administrator can:

- manage formats, published posts, drafts, tags, related posts, and ordered files;
- edit type-specific metadata through validated fields rather than raw JSON;
- upload files individually, paste a clipboard image, or upload many files with
  an optional label prefix and image-compression choice;
- edit file labels without changing stored paths, and inspect originals/previews;
- find files unused by posts or covers and delete selected records normally;
- confirm removal of unreferenced physical files and rebuilding of post-file
  labels; these maintenance operations are reserved for the site owner;
- export tag/file metadata through superuser-only read APIs.

GIF originals retain their animation. Image compression can be disabled during
bulk upload; thumbnails are generated in either mode. Deleting a database file
record does not immediately delete its stored bytes. Profile references do not
protect files from cleanup: the owner attaches them to a service post.

## Shared presentation and discovery

The interface works on desktop and mobile. Media preserves its natural aspect
ratio in detail views; carousels stop at either end and leave browser keyboard
shortcuts intact. Card previews use the main file, or the first ordered
additional file when the main file is absent. Every page ends with a year footer.

Post labels prefer the name, then a text excerpt, then attached-file counts,
with a neutral fallback for empty posts. Page-specific titles and social
metadata follow visibility and draft rules. The sitemap includes the home,
archive, and public format pages, excluding private formats and individual
posts. Crawler rules advertise the sitemap and allow public Telegram previews.

## HTTP status playground

`/r/<code>/` serves public synthetic HTTP examples and jokes, including redirects
and selected nonstandard statuses. It supports GET/HEAD, does not change site
data, and is not cached or indexed. Unsupported codes return 404. Individual
response bodies and protocol examples are defined in the handlers.
