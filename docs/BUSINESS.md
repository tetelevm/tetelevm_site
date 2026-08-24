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
- browse public projects;
- view all items in public projects;
- open the guest login page.

Anonymous access is read-only.

### Guest

A guest is a trusted visitor using shared access provided by the site owner.
A guest can do everything available to an anonymous visitor and can also view
private projects and their items. An authenticated guest can sign out and
return to anonymous access.

Guest access is read-only. Guests cannot create, edit, upload, or delete
content. Separate guest profiles are not required.

### Administrator

The administrator is the site owner. The administrator can:

- create and manage projects;
- create and edit project items;
- edit type-specific item metadata through individual validated fields instead
  of raw JSON;
- upload media used by the content, including many files in one operation;
- optionally prepend one shared string to every original-name label during a
  multi-file upload;
- choose during a multi-file upload whether image originals are resized and
  compressed; previews and thumbnails are generated in either mode;
- edit the original-name label of an uploaded file without renaming its stored
  content;
- see generated image thumbnails directly in the administrative file list and
  post-file inlines, and a larger preview on an image file's change page;
- mark projects as public or private;
- find related posts in the administrative selector by project name and post
  number, including combined queries such as `погулялки #10`;
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
landing page shows projects, not a single feed mixing unrelated items. Each
project is an independent collection with its own list of material and may use
a presentation suited to its purpose.

Opening `/archive/random/` selects a random post from the material visible to
the current visitor and opens that post. Anonymous visitors are never sent to
private projects; authenticated guests and administrators may receive either
public or private posts.

Unknown public URLs and missing projects or posts show a localized not-found
page instead of redirecting to the home page. It offers a `ru/en` switch and a
link that opens a random post visible to the current visitor.

### Login

The site provides a login page matching its own interface. Its main purpose is
to give trusted visitors access to private projects. Ordinary visitors should
not be directed to an administrative login screen. Valid guest and administrator
credentials create a normal site session; authenticated visitors can sign out
from the public interface.

The shared header shows the site logo on every page. Three quick activations of
the logo reveal the login or logout control in its place. The login URL remains
directly accessible.

## Content organization

Content follows this hierarchy:

```text
Content -> Project -> Item
```

A project determines:

- the collection to which an item belongs;
- a short description shown above its material;
- whether the collection is public or private;
- the general presentation of its material.

Project cards communicate lifecycle status separately from visibility. Open
projects have no status label, paused projects show “на паузе” in a warm
yellow-orange color, and closed projects show “завершён” in red. Private
projects are not dimmed; a small gray lock in the top-left corner of the cover
communicates their visibility without a written status label.
The project page repeats a paused or closed status beside its material count,
using the same warm or red status color; open projects show only the count.
Each project card shows its total number of posts in a small circle at the
bottom-left of its cover.

An item contains the actual material, such as text, images, video, or a
combination of media. The supported project presentation types and their visual
behavior are specified in `docs/PROJECT_TYPES.md`.

An abandoned-building post may include linked latitude and longitude. When all
location values are present, the coordinates appear as an external map link
directly below the post title and above its text.
An anime post may include a season string. When present, it appears in italics
immediately after the post name on the same title line.
General posts display their body as plain text by default. An optional boolean
flag enables Markdown rendering for an individual general post.
Posts may be connected to any number of other posts through symmetric
relationships. Detail pages show every related post visible to the current
visitor as a row card; links to private content remain hidden from anonymous
visitors.
At the bottom of every post detail page, navigation links point to the nearest
lower-numbered and higher-numbered posts in the same project. Missing numbers
are skipped, and a link is omitted at the corresponding project boundary. The
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
neutral fallback symbol. Image-only project presentations may omit the visible
label while retaining it as the image's accessible description.

## Visibility

Visibility is defined at project level:

- public projects and all their items are available without authentication;
- private projects and all their items are hidden from anonymous visitors;
- authenticated guests can view both public and private projects.

Items do not have independent visibility settings. Per-item visibility should
only be introduced if a future product requirement needs it.

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
devices. Detailed visual design and the presentation of individual project
types will be defined separately as the corresponding content is designed.
Standalone media frames and carousels show images without cropping and follow
their natural aspect ratio. Carousels resize when one gallery mixes portrait
and landscape media.
Carousel navigation stops at the first and last item and does not capture the
keyboard arrow keys used by browser shortcuts. While the next image loads, the
carousel retains the current frame's size and then resizes directly to the new
aspect ratio, avoiding an intermediate collapse that disrupts page scrolling.
Post card lists use a single framed surface for the image and, when present,
its caption and rating. Image-only cards keep the same frame without an empty
caption area.
Every public page ends with a small footer showing the current year.
