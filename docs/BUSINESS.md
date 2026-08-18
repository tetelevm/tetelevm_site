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
- upload media used by the content;
- mark projects as public or private;
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

The Content landing page shows projects, not a single feed mixing unrelated
items. Each project is an independent collection with its own list of material
and may use a presentation suited to its purpose.

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

An item contains the actual material, such as text, images, video, or a
combination of media. The supported project presentation types and their visual
behavior are specified in `docs/PROJECT_TYPES.md`.

Every post has a shared label for list and administrative displays. It uses the
post name when available, otherwise the beginning of its text, otherwise a
summary of attached file types. A completely empty post uses a neutral fallback
symbol.

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
Every public page ends with a small footer showing the current year.
