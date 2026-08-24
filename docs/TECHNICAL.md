# Technical Architecture

## Scope and status

The repository contains a working Django REST Framework, Vue, Vue Router, Vite,
PostgreSQL, and Docker Compose application. The first frontend prototype is
implemented and builds successfully. Domain models and read-only project API
endpoints, project-grid integration, session authentication, media processing,
and a single-server production deployment exist.

This document describes the intended architecture. A capability mentioned here
should not be treated as already implemented unless it exists in the codebase.

## Repository layout

```text
/
├── backend/       Django, REST API, administration, and backend tests
├── frontend/      Vue application and frontend tests
├── media/         Persistent uploaded media (contents ignored by Git)
├── deploy/        Container and production deployment configuration
├── docs/          Product and technical documentation
├── scripts/       Maintenance and operational automation
├── compose.yaml   Local development orchestration
├── AGENTS.md      Instructions for coding agents
└── README.md      Project overview and setup
```

The `scripts/` directory is reserved for repository-level maintenance and
operational tasks, such as backups, restores, data imports, release helpers, or
deployment automation. Application code and reusable Django or Vue logic do not
belong there. Scripts should be added only when a real repeated operation needs
automation.

The project is a monorepo. It is deliberately optimized for clarity and simple
operation rather than independent service deployment or high traffic.

## Production deployment

Production is designed for one low-traffic Debian or Ubuntu VPS. The separate
`compose.prod.yaml` runs PostgreSQL, Django under a single Gunicorn worker with
two threads, and Caddy. Caddy is the only publicly exposed service. It obtains
and renews TLS certificates, serves the built Vue application and persistent
media, serves collected Django static files, and proxies API and admin requests
to Django. PostgreSQL and Gunicorn do not publish host ports.

The production frontend image builds Vue once with Vite and copies the output
into the Caddy image; Node and the Vite development server do not run in
production. PostgreSQL data, collected static files, and Caddy state use named
volumes. Uploaded media remains a bind-mounted repository-root `media/`
directory so it can be backed up and restored alongside the database.

Production configuration is supplied by an ignored `.env.production` file.
HTTPS-related Django settings remain environment-driven so local development
continues to use HTTP. Operational commands and backup requirements are in
`docs/DEPLOYMENT.md`.

## System boundaries

The Vue application is the public user interface. It communicates with Django
through a small REST API.

Django is responsible for:

- persistence and domain rules;
- authentication state and authorization;
- project and content visibility;
- administrative content management;
- media metadata and file handling;
- exposing safe data through the REST API.

Vue is responsible for:

- public routing and presentation;
- the custom guest login experience;
- responsive desktop and mobile layouts;
- rendering projects and items according to their presentation type.

The shared public header loads the session state once. When `isStaff` is true,
it shows a localized icon link to `/_admin/`; Django continues to enforce staff
authorization at the destination.

Frontend filtering is presentation logic, not a security boundary.

## Backend

The backend uses Python, Django, Django REST Framework, PostgreSQL, and Django
Admin.
User-facing backend labels use Django gettext localization, with Russian
translations stored in the repository and compiled during development or
deployment builds.

Backend domain code is grouped into two Django applications: `core` contains
shared models such as uploaded files, while `projects` contains projects and
their content items.

Django Admin is the primary authoring interface. A broad write API is therefore
unnecessary. The REST API should remain small and be expanded in response to
actual frontend use cases.

The post admin excludes the raw `extra` JSON field and exposes explicit virtual
form fields for the supported type-specific metadata. `PostAdminForm` selects
the applicable fields from the chosen project's `post_type`, applies numeric
ranges and required-field validation, and serializes the cleaned values back
into `Post.extra`. Anime and abandoned-building ratings use separate form
fields because one is an integer from 1 through 10 and the other is a float
from 1 through 5, although both remain `extra.rating` in storage. Known fields
from other post types are removed when saving; unrecognized top-level and
nested location keys are retained to avoid accidental data loss.

A small admin script receives the project-to-post-type map from a data attribute
on the project widget's inner `<select>`, then enables and marks required only
the relevant metadata fields as the project changes. The attribute is assigned
to the inner widget explicitly because Django Admin wraps related fields in a
`RelatedFieldWidgetWrapper`. All supported metadata controls remain visible
together in one dedicated fieldset, with inapplicable fields disabled. Every
post field occupies its own form row.
Dedicated admin CSS makes the name input wider, caps the related-post
autocomplete at 700 pixels, and keeps both autocomplete fields responsive on
mobile.

For general posts the Markdown checkbox writes a JSON boolean; the detail
component uses `MarkdownContent` only when it is `true` and otherwise keeps the
plain-text renderer. Anime's optional `season` is rendered inline in italics
after the post name; `PostTitle` places an explicit line-break opportunity
before it so the suffix wraps independently. Abandoned posts store `latitude`,
`longitude`, and `link` below a nested `location` key. Their Vue detail
component renders complete locations as an `http(s)` external link and ignores
incomplete or unsafe values.

Relations to potentially large collections use Django Admin's built-in AJAX
autocomplete widgets. They keep the default 20-result pages and load further
results on scroll. File choices are searchable by original upload name and ordered
by newest upload first. The main file changelist displays existing image
thumbnails inline at 64 by 64 pixels and leaves the preview cell empty for
non-image files. An image file's change page shows its aspect-ratio-preserving
600-pixel preview. A saved file's `original_name` can be edited as display
metadata without renaming or moving stored content; during initial upload it is
still derived from the browser-provided filename. The standard file-add form
has a focusable clipboard area whose browser-side paste handler converts one
clipboard image into a named `File` object and assigns it to the native content
input before normal multipart submission. The file changelist also links to an admin-only bulk upload
form that accepts multiple browser-selected files and creates one `File` record
per upload using the model's media-processing path. A checked-by-default option
normalizes image originals through the usual 1500-pixel JPEG conversion; when
unchecked, the uploaded original bytes and extension are retained while preview
and thumbnail derivatives are still generated. Its optional prefix
is prepended to each resulting `original_name` after processing and therefore
does not affect stored UUID paths or file-type detection. The post changelist
places the project column before the post number and display label. Saved `PostFileInline`
rows show 64-pixel thumbnails and use
`select_related("file")` to avoid per-row queries; post choices are ordered by
descending database ID.
Post choices and the post changelist use the same derived display label as the
public lists. Post search also covers the project name and exact post number;
an isolated hash before digits is removed so combined autocomplete queries such
as `погулялки #10` use Django Admin's normal per-term matching.

Expected read capabilities include:

- current authentication state when needed by the interface;
- projects visible to the current user;
- details and items for a selected project;
- individual item details when required by a project type.

## Authentication and authorization

Use Django's standard user and session authentication. The initial account model
contains:

- anonymous visitors with access to public content;
- one non-staff shared guest account with access to private content;
- the site owner's staff or superuser account for administration.

Do not introduce JWT or a custom authentication framework without a client or
deployment requirement that makes session authentication unsuitable.

Authorization must be enforced in backend API views. Anonymous API
requests must not reveal private projects or items belonging to them. The
frontend renders only the projects returned by the backend and must not be
responsible for filtering private data.

CSRF protection is required for login, logout, and every state-changing
operation. The frontend obtains a token from `/_api/auth/csrf/` and sends it in
the `X-CSRFToken` header for login and logout. Current project endpoints are
read-only. Future session-authenticated writes must use the same protection.
Development frontend origins are supplied through
`DJANGO_CSRF_TRUSTED_ORIGINS`; production should set this variable to its real
HTTPS origin when the frontend and backend are not seen as the same origin.

## Content domain

The project domain currently uses these models:

```text
Project
    name
    description: optional short text
    link: unique string
    cover -> File
    post_type: fixed presentation type
    post_list_type: fixed presentation type
    is_public
    status: open | paused | closed
    order

Tag
    code: unique string
    name

Post
    project -> Project
    number: unique within project
    optional date
    link: /archive/<project link>/<number>/
    optional name and text
    optional main_file -> File
    extra: JSON
    related_posts -> Post (symmetric many-to-many)
    files -> File through ordered PostFile
    tags -> Tag
```

A project is an independent content collection. It owns the visibility and
presentation context inherited by its posts. Detail presentation types use the
explicit `post`, `photo`, `travel`, `text`, `text_md`, `door`, `anime`,
`plasticine`, and `abandoned` choices. List presentation is independent and
uses reusable card choices: `row_card`, `photo_card`, `label_photo_card`, and
`rated_photo_card`. A post belongs to exactly one project; its number determines
its position and is unique within that project.
Additional post files are connected through `PostFile`, which stores their
order. Post relationships use Django's implicit self-referential many-to-many
table and are symmetric: adding either side makes the other side related too.
Avoid a generic page builder or universal CMS schema without a demonstrated
need.

`Post.display_label` is the single source for list and administrative labels. It
prefers a trimmed name, then a whitespace-normalized 90-character text excerpt,
then counts of unique files by media type, and finally `🌀`. A custom
`PostQuerySet.with_display_file_counts()` method annotates the four per-type
counts. List API and admin querysets opt into it explicitly, avoiding per-post
queries without adding aggregation overhead to unrelated post queries.
`PostQuerySet.with_adjacent_post_ids()` uses correlated subqueries scoped by
`project_id` to annotate the nearest lower-numbered and higher-numbered post
IDs. Gaps in numbering therefore require no special handling.

Project status describes its lifecycle and does not control authorization.
Project cards show no badge for `open`, a warm yellow-orange “на паузе” badge
for `paused`, and a red “завершён” badge for `closed`. Private cards remain
dimmed but do not display a visibility badge. Visibility for anonymous and
authenticated visitors continues to depend only on `is_public`.

The backend should expose an explicit presentation type. The frontend should
map that type to a known Vue component. Keep this mapping simple and visible in
the codebase.

## User-facing routes

The intended routes are:

```text
/                               About
/login/                         Guest login
/archive/                       Projects visible to the visitor
/archive/random/                Open a random visible post
/archive/<project>/             Items in a project
/archive/<project>/<item>/      Item detail when the project needs one
/<unknown path>                 Localized not-found page
```

Exact identifiers and slug behavior remain deferred. The Content landing page
must remain project-oriented rather than becoming a global mixed feed.

## Internal routes

Internal and operational HTTP routes use an underscore prefix to distinguish
them from the public site structure. Current routes are:

```text
/_admin/                       Django Admin
/_api/auth/csrf/               CSRF token and cookie
/_api/auth/session/            Current authentication state
/_api/auth/login/              Session login
/_api/auth/logout/             Session logout
/_api/random-post/             Link to a random post visible to the visitor
/_api/projects/                Projects visible to the current visitor
/_api/projects/<project>/      Project metadata and paginated posts (`?page=N`)
/_api/projects/<project>/<n>/  Individual post
/_static/                      Django-managed static assets
```

Future internal endpoints should follow the same `/_name/` convention. Public
pages such as `/`, `/login/`, and `/archive/` do not use this prefix.

The random-post endpoint applies the same project-visibility queryset as the
other read APIs before selecting a post. The Vue random route replaces its own
history entry with the returned canonical post link, so refresh and sharing use
the selected post URL rather than drawing another random result.

## Media

Initial uploads are managed through Django Admin and stored in the repository
root `media/` directory, whose contents are ignored by Git. Compose mounts it at
`/media` in the backend container. Production deployment must preserve this
directory independently of container replacement.

Uploaded files are represented by the `File` model, retain their upload name in
`original_name`, and store `file_type` as `photo`, `video`, `audio`, or `other`.
The type is detected from the extension when a new file is uploaded. Stored
files use the model UUID and are separated by role:
non-image originals use `content/<UUID>.<extension>`, normalized image originals
use `content/<UUID>.jpg`, image previews use
`preview/<UUID>.jpg`, and image thumbnails use `thumbnail/<UUID>.jpg`.
Image originals are normally normalized to metadata-free JPEG at 90 percent
quality and constrained to 1500 pixels on each axis without upscaling. Bulk
upload can explicitly retain the uploaded original instead. Previews are
metadata-free JPEGs constrained to 600 pixels on each axis without upscaling.
Thumbnails are metadata-free 150-by-150 JPEGs produced with a centered square
crop and are upscaled when the source is smaller. Replacing an uploaded image
regenerates the original, preview, and thumbnail. For images, `link`
points to the preview, `link_small` to the thumbnail, and `link_full` to the
original; non-images use the original for both `link` and `link_small` and have
no `link_full`. Django serves these URLs only in debug mode; production
must serve `MEDIA_ROOT` at `/files/` through the reverse proxy.
The Vite development server also proxies `/files/` to Django. Project cards
render covers in a square container and center-crop non-square images.

External embeds or media providers may be added when a concrete content type
requires them. They are not part of the initial infrastructure.

## Frontend

The frontend uses Vue, Vue Router, and Vite. Public pages, including login,
belong to Vue. Different project types may use different components, but the
application should not become a runtime page-builder.

Markdown post text is rendered client-side with `markdown-it`. The `text_md`
type always uses it, while the general `post` type opts in per item through
`extra.md === true`. Embedded raw HTML is disabled; Markdown-generated markup
is styled by the dedicated `MarkdownContent` component. The
`markdown-it-container` plugin provides safe `::: spoiler [title]` containers,
rendered as native `details` and `summary` elements while their body continues
to support Markdown. Project descriptions reuse the same `MarkdownContent`
component in `PageSubheader`, including spoiler support and raw-HTML blocking.

The current router implements:

```text
/                About-page construction notice
/archive/                       Projects loaded from the REST API
/archive/:project/              Project posts loaded from the REST API
/archive/:project/:postNumber/  Individual post loaded from the REST API
/login/          Session login
```

The shared frontend building blocks are:

- `MainLayout` for the global background, shared header, and centered
  800-pixel content container;
- `AppFooter` for the shared current-year footer;
- `AppHeader` for navigation and a page-specific action slot;
- `LanguageSwitch` for the About-page `ru/en` control;
- `HeaderAccessAction` for the site logo and concealed login/logout control;
- `LoginLink` for the login/logout icon revealed by the header logo;
- `ProjectGrid` for a responsive grid of at most three cards per row;
- `ProjectCard` for post counts, lifecycle-status badges, and visually dimmed
  private states.
- `PostCardList` for rendering framed square-image cards with an optional
  caption and rating section inside `list-types`;
- `RatedPostHeader` for detail types whose title sits beside an overall rating.
- `PostRowList` for rendering rows with a media slot, label, and date inside
  `list-types`;
- `PostLayout` for the shared vertical composition and spacing of detail posts;
- `PostTitle` for shared detail-title and optional subtitle typography;
- `DatedPostHeader` and `RatedPostHeader` for compositions of `PostTitle` with
  right-side metadata;
- `PlainPostText` for consistently styled plain-text post bodies;
- `PostImage` for aspect-ratio-preserving natural-size or framed standalone
  images, optionally using the shared lightbox;
- `MarkdownContent` for styled, HTML-disabled Markdown rendering.
- `PostTag` for non-interactive tag labels on post detail pages;
- `PostConnections` for adapting related-post summaries to `PostRowList` and
  rendering tags; `PostPage` uses it for related posts after every detail-type
  body, while the applicable type components use it locally for tags;
- `PostNavigation` for the previous and next post links at the bottom of every
  detail page;
- `PostFileList` for non-image and non-video file links using original names.
- `PageStatus`, `PageSubheader`, and `PaginationNav` for shared page-level
  feedback, secondary navigation, and pagination presentation.

Frontend components are grouped by responsibility rather than kept in one flat
directory:

```text
components/
├── auth/                 concealed login/logout controls
├── common/               reusable page-level UI
├── layout/               global header, footer, and page shell
├── media/                lightbox and bounded, adaptive media carousel
├── posts/
│   ├── blocks/           reusable detail-post building blocks
│   ├── lists/            base card and row renderers
│   ├── list-types/       type-specific list data adapters
│   └── types/            detail-post compositions
└── projects/             project cards, grid, and header action
```

`MediaCarousel` records the loaded active item's intrinsic aspect ratio. It
keeps that ratio as the stage reservation while the next item loads, then
updates the stage once from the new image or video dimensions. This avoids an
intermediate zero-height layout without adding media dimensions to the API.

Detail post responses expose `relatedPosts` as an array containing each visible
related post's ID, number, model-generated link, display label, optional photo
thumbnail, and date. The relation prefetch applies the same project-visibility
rules as normal post access, annotates display-label file counts, and prefetches
thumbnail candidates so rendering multiple related cards does not cause N+1
queries. Results use project order followed by descending post number. The
`PostPage` places these summaries after every type-specific body and passes them
through the shared `PostRowList` renderer before adjacent-post navigation; it
does not reconstruct backend routes.
The detail queryset also annotates adjacent post IDs. The view loads both
adjacent objects together with annotated display-label counts and exposes them
as nullable `previousPost` and `nextPost` summaries containing `number`, `link`,
and `label`. `PostPage` renders those summaries below the type-specific content,
using the current project name in the link text. `PostNavigation` truncates only
the visible label portion to 80 Unicode characters, retains the full value in
the accessible link label, permits breaks inside uninterrupted strings, and
frames each complete link rather than its arrow alone. It renders `nextPost`
first on the left and `previousPost` second on the right, retaining the same
order when the layout collapses to one column. `PlainPostText` and
`MarkdownContent` apply the same overflow protection to post bodies.

Projects are returned in ascending explicit project order. Posts within a
project are returned by descending post number, with the highest-numbered item
first.

The project-posts page fetches a project and its posts from the REST API, then
uses an explicit mapping from the project's `postListType` code to a component in
`components/posts/list-types`: `row_card` uses `RowCard`, `photo_card` uses
`PhotoCard`, `label_photo_card` uses `LabelPhotoCard`, and `rated_photo_card`
uses `RatedPhotoCard`. Each adapter receives the project's `posts`
array and maps the relevant fields into display data for `PostCardList` or
`PostRowList`. Those two base renderers live beside the adapters and do not
inspect API post shapes. List entries contain only the fields required by the
adapters;
they do not expose `extra`, additional files, tags, or detail-page metadata.
Every list response includes the model-derived `label`. List `mainFile` data
includes the stored `mediaType` so presentation types can distinguish photos,
videos, audio, and other files without filename parsing.
The image-only `photo_card` adapter uses the label for accessible image text but
passes no visible caption to `PostCardList`. `plasticine` now shares the visible
label presentation used by `door`.
Post dates come from the optional model field rather than `extra`. PostgreSQL
extracts only `rating` from `extra` for its dedicated list field. General post
lists use the same `mainFile` summary as every other list type and do not search
additional files for a thumbnail. All list types use one list serializer and
standard square thumbnails. Project posts use
page-number pagination with 48 posts per page;
the response includes the current page, page size, total pages, and total posts.
The frontend keeps the selected page in the URL query string and renders numeric
page controls.

The individual-post page selects its component through an explicit mapping from
the API's `postType` value. Both list and detail mappings live together in
`frontend/src/config/postTypes.js`, keeping the supported type registry explicit.
Concrete type components compose shared presentation blocks while retaining
their own data selection and type-specific markup. This is deliberately a set
of static Vue compositions, not a runtime page-builder. Concrete list and post
presentation behavior is specified in `docs/PROJECT_TYPES.md`.

Projects come from the REST API. Anonymous users never receive private projects;
authenticated guests receive them with `isPublic: false` so their cards can be
dimmed. The separate `status` field controls the lifecycle badge. Project list
and project-post querysets annotate their post total as `post_count`; the shared
serializer exposes it as `postCount`, and the project card renders it on the
bottom-left of the cover. Because aggregation drops Django's implicit model
ordering, the annotated query explicitly reapplies ascending `order` and `id`.
The authorization queryset remains unannotated.

The login form uses Django session authentication with CSRF protection and
redirects successful logins to the project grid. The header action reflects the
current session and provides logout. The About-page language switch stores its
selection only in component state. It translates that page's construction
notice, navigation labels, and footer, but does not persist the selection or
translate project content.

Global frontend styling uses a dark editorial palette defined through CSS
custom properties, a compact pill-based header, serif display headings, and a
system sans-serif text stack. Cards use square center-cropped covers, restrained
motion, visible focus states, and responsive grids. Page-specific styles remain
scoped to Vue components. The favicon is stored in
`frontend/public/favicon.ico`.

On project and post pages, the current project name appears beside the site
logo in the header. Three quick logo activations replace it with the session
action. A compact subheader row directly below contains the back link and, on
project lists, the total item count and optional short project description.

Frontend testing should be proportional to the amount of meaningful client-side
logic. Static presentation does not require exhaustive component tests.

## Testing

Use pytest and pytest-django for backend tests unless a concrete constraint
requires another tool. Prioritize behavior with security or domain significance:

- anonymous users cannot retrieve private projects or their items;
- guests can retrieve private projects and remain read-only;
- guest users cannot obtain staff or administrative capabilities;
- visibility is applied consistently to every item in a project;
- REST API views enforce authorization;
- login, logout, and session behavior work correctly;
- core model invariants are preserved.

## Development and deployment

Local development uses the root `compose.yaml` with three services:

- `frontend` for the Vite development server;
- `backend` for the Django development server;
- `db` for PostgreSQL.

The frontend service runs `npm install` before Vite because `node_modules` is a
persistent Docker volume. This keeps newly added package dependencies in sync
without requiring manual volume removal.

The production target is a conventional VPS using Docker Compose, persistent
PostgreSQL and media volumes, and a reverse proxy that terminates HTTPS and
routes traffic to the frontend and backend. The production application server,
reverse proxy, static asset strategy, backups, and release procedure remain to
be selected and implemented.

Secrets and production credentials must be supplied through environment
configuration and must never be committed to the repository.

## Deliberate non-goals

The initial architecture does not require horizontal scaling, Kubernetes,
Redis, Celery, message brokers, separate services for content types, complex
RBAC, per-item access rules, or a generic CMS/page-builder. Revisit these
choices only when a concrete requirement makes one of them useful.

## Deferred decisions

The following are intentionally unresolved:

- exact Django model fields and remaining API response fields;
- storage for heterogeneous item content;
- detailed visual design and SEO strategy;
- external media and embed support;
- production application server and reverse proxy;
- backup and deployment procedures;
- which About-page fields, if any, should be editable.

## Suggested next stage

The next coherent milestone is backend-driven Projects and authentication:

1. define the minimal `Project` model and Django Admin configuration;
2. expose only projects visible to the current user through the REST API;
3. add authorization tests before exposing any private project data or items;
4. replace the temporary array in `ProjectsPage.vue` with a REST API request;
5. implement session login and logout with correct CSRF handling;
6. connect the login form and header state to the authenticated session.
