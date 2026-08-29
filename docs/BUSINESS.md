# Product Requirements

## Purpose

This project is the site owner's personal website. It combines a personal
presentation page with a publishing and archive area for the owner's material.

The site is intended primarily for reading and viewing. It is not a social
network, a public publishing platform, or a general-purpose CMS.

## Audience and roles

### Anonymous visitor

An anonymous visitor can:

- view the About page;
- browse public formats;
- view all items in public formats;
- open the guest login page.

Anonymous access is read-only.

### Guest

A guest is a trusted visitor using shared access provided by the site owner.
A guest can do everything available to an anonymous visitor and can also view
private formats and their items. An authenticated guest can sign out and
return to anonymous access.

Guest access is read-only. Guests cannot create, edit, upload, or delete
content. Separate guest profiles are not required.

### Administrator

The administrator is the site owner. The administrator can:

- create and manage formats;
- create and edit format items;
- edit type-specific item metadata through individual validated fields instead
  of raw JSON;
- upload media used by the content, including many files in one operation;
- optionally prepend one shared string to every original-name label during a
  multi-file upload;
- choose during a multi-file upload whether image originals are resized and
  compressed; thumbnails are generated in either mode;
- paste a clipboard image into the standard administrative file-add form as an
  alternative to selecting it through the browser;
- edit the original-name label of an uploaded file without renaming its stored
  content;
- open the stored original from a direct path link shown first on the file's
  administrative change page;
- see generated image thumbnails directly in the administrative file list and
  post-file inlines, and a larger preview on an image file's change page;
- mark formats as public or private;
- find related posts in the administrative selector by format name and post
  number, including combined queries such as `погулялки #10`;
- open Django Admin from a staff-only icon in the public site header;
- manage the site through an administrative interface.

## Main areas

### About

The root page presents the site owner. It may contain biographical information,
contacts, photographs, and other personal presentation blocks.

Most of this page is expected to be relatively static. Individual parts may be
made editable when there is a practical need.

Until the presentation content is ready, the page shows a short localized
notice that it is still under construction.

The About page provides a compact `ru/en` language switch in its header. It
switches the construction notice, main navigation labels, and footer between
Russian and English for the current page visit; the selection is not persisted.

### Content

The Content area contains material created by the site owner, including
articles, notes, photographs, anime write-ups, long-form text, and media
publications.

The public section is named “Archive” and is available at `/archive/`. Its
landing page shows formats, not a single feed mixing unrelated items. Each
format is an independent collection with its own list of material and may use
a presentation suited to its purpose.
The Archive landing page metadata describes it as an archive of the owner's
formats, texts, photographs, and other material.

Search engines can discover the home page, Archive landing page, and public
format pages through a sitemap. Private formats and individual posts are not
listed. Crawler instructions point to that sitemap and discourage crawling of
the administrative and API routes. They explicitly allow Telegram's link
preview bot to access public pages.

Public pages expose page-specific browser titles and social-link metadata.
Format metadata uses the format's localized name, description, and cover.
Post metadata uses its name when present or its format and number otherwise;
its description uses a text excerpt or attached-file counts, and its image uses
the stored main photo with the site favicon as a fallback.

Opening `/archive/random/` selects a random post tagged with the special
`star` code from the material visible to the current visitor and opens that
post. Anonymous visitors are never sent to private formats; authenticated
guests and administrators may receive either public or private starred posts.

Unknown public URLs and missing formats or posts show a localized not-found
page instead of redirecting to the home page. It offers a `ru/en` switch and a
link that opens a random starred post visible to the current visitor. The response uses
the real HTTP 404 status and is excluded from search indexing. Switching the
language also updates the document language, page title, description, and
social metadata for the current visit.

### Login

The site provides a login page matching its own interface. Its main purpose is
to give trusted visitors access to private formats. Ordinary visitors should
not be directed to an administrative login screen. Valid guest and administrator
credentials create a normal site session; authenticated visitors can sign out
from the public interface.

The shared header shows the site logo on every page. Three quick activations of
the logo reveal the login or logout control in its place. The login URL remains
directly accessible.

## Content organization

Content follows this hierarchy:

```text
Content -> Format -> Item
```

A format determines:

- the collection to which an item belongs;
- a Markdown description shown above its material, including optional
  click-to-expand spoiler blocks;
- whether the collection is public or private;
- the general presentation of its material.

Format cards communicate lifecycle status separately from visibility. Open
formats have no status label, paused formats show “на паузе” in a warm
yellow-orange color, and closed formats show “завершён” in red. Private
formats are not dimmed; a small gray lock in the top-left corner of the cover
communicates their visibility without a written status label.
The format page repeats a paused or closed status beside its material count,
using the same warm or red status color; open formats show only the count.
Each format card shows its total number of posts in a small circle at the
bottom-left of its cover.

An item contains the actual material, such as text, images, video, or a
combination of media. The supported format presentation types and their visual
behavior are specified in `docs/PROJECT_TYPES.md`.

An abandoned-building post may include linked latitude and longitude. When all
location values are present, the coordinates appear as an external map link
directly below the post title and above its text.
An anime post may include a subtitle string. When present, it appears in italics
immediately after the post name on the same title line.
General posts display their body as plain text by default. An optional boolean
flag enables Markdown rendering for an individual general post.
Posts may be connected to any number of other posts through symmetric
relationships. Detail pages show every related post visible to the current
visitor as a row card; links to private content remain hidden from anonymous
visitors.
Posts can be marked as drafts in Django Admin. Drafts are administrative-only:
they are excluded from format lists and counts, tag filters, random selection,
related and adjacent navigation, direct post URLs, and page metadata for every
public-site visitor, including authenticated guests and administrators.
Post tags are links to the current format with a `tag=<code>` query parameter.
Opening one shows only posts in that format carrying the selected tag; list
pagination retains the filter. The active filter appears between the format
description and its posts using the same tag-chip presentation as post tags. It
shows the tag's configured name when the code exists and the requested code as
a fallback.
At the bottom of every post detail page, navigation links point to the nearest
lower-numbered and higher-numbered posts in the same format. Missing numbers
are skipped, and a link is omitted at the corresponding format boundary. The
forward link to the higher-numbered post appears first on the left, while the
back link to the lower-numbered post appears second on the right; on mobile they
keep that top-to-bottom order. The
visible label excerpt is limited to 80 characters and wraps even when it
contains no natural break points. Each entire neighboring-post link is enclosed
in a frame. Post body text also remains within the content width when it
contains a long uninterrupted string.

Every post has a shared label available to list and administrative displays. It
uses the post name when available, otherwise the beginning of its text,
otherwise a summary of attached file types. A completely empty post uses a
neutral fallback symbol. Image-only format presentations may omit the visible
label while retaining it as the image's accessible description.

## Visibility

Visibility is defined at format level:

- public formats and all their items are available without authentication;
- private formats and all their items are hidden from anonymous visitors;
- authenticated guests can view both public and private formats.

Items do not have independent audience visibility settings. The draft flag is
an authoring-state exception that hides an item from every public-site role.
Per-item audience permissions should only be introduced if a future product
requirement needs them.

## Interaction model

The site is consumption-oriented. The initial product does not include:

- public registration;
- comments;
- likes or reactions;
- visitor-created content;
- editing by guests;
- separate guest accounts or profiles.

These features should not be assumed merely because they are common on blogs or
publishing platforms.

## User experience

The public interface must be usable and visually coherent on desktop and mobile
devices. Detailed visual design and the presentation of individual format
types will be defined separately as the corresponding content is designed.
Standalone media frames and carousels show images without cropping and follow
their natural aspect ratio. Carousels resize when one gallery mixes portrait
and landscape media.
Post detail pages load the stored image original directly. Separate generated
medium-sized previews are not retained; square thumbnails remain available for
list cards and administrative lists.
Structured post files use their stored media type to select an image, video,
audio, or download-link presentation. Embedded Markdown media infers the same
presentation from the URL extension used in image syntax.
Carousel navigation stops at the first and last item and does not capture the
keyboard arrow keys used by browser shortcuts. While the next image loads, the
carousel retains the current frame's size and then resizes directly to the new
aspect ratio, avoiding an intermediate collapse that disrupts page scrolling.
Post card lists use a single framed surface for the image and, when present,
its caption and rating. Image-only cards keep the same frame without an empty
caption area.
Every post-card presentation uses the main file as its preview source. When it
is missing, the first ordered additional file used by the post carousel becomes
the shared card preview source; non-image files still leave image preview slots
empty.
Every public page ends with a small footer showing the current year.
