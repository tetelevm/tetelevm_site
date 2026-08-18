# Technical Architecture

## Scope and status

The repository contains a working development foundation: Django REST Framework,
Vue, Vue Router, Vite, PostgreSQL, and Docker Compose. The first frontend
prototype is implemented and builds successfully. Domain models and read-only
project API endpoints, project-grid integration, and session authentication
exist. Broader media integration and production deployment are still to be
implemented.

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

The post admin keeps `extra` as a validated raw JSON textarea. A small admin
script prepopulates it from an explicit `post_type` template when the project is
selected. It may replace a previously auto-applied template but never overwrites
manually edited JSON. The project-to-template map is embedded in the form; this
is intentionally simpler than an additional endpoint for the site's small
project collection.

Relations to potentially large collections use Django Admin's built-in AJAX
autocomplete widgets. They keep the default 20-result pages and load further
results on scroll. File choices are searchable by original upload name and ordered
by newest upload first; post choices are ordered by descending database ID.

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
    link: /projects/<project link>/<number>/
    optional name and text
    optional main_file -> File
    extra: JSON
    optional related_post -> Post
    files -> File through ordered PostFile
    tags -> Tag
```

A project is an independent content collection. It owns the visibility and
presentation context inherited by its posts. Its post and post-list presentation
types use separate explicit choice lists, currently containing `post`, `photo`,
`travel`, `text`, `text_md`, `door`, `anime`, `plasticine`, and `abandoned`
options. A post belongs to exactly one project; its number determines its
position and is unique within that project.
Additional post files are connected through `PostFile`, which stores their
order. Avoid a generic page builder or universal CMS schema without a
demonstrated need.

Project status describes its lifecycle and does not control authorization.
Visibility for anonymous and authenticated visitors continues to depend only
on `is_public`.

The backend should expose an explicit presentation type. The frontend should
map that type to a known Vue component. Keep this mapping simple and visible in
the codebase.

## User-facing routes

The intended routes are:

```text
/                               About
/login/                         Guest login
/projects/                      Projects visible to the visitor
/projects/<project>/            Items in a project
/projects/<project>/<item>/     Item detail when the project needs one
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
/_api/projects/                Projects visible to the current visitor
/_api/projects/<project>/      Project metadata and paginated posts (`?page=N`)
/_api/projects/<project>/<n>/  Individual post
/_static/                      Django-managed static assets
```

Future internal endpoints should follow the same `/_name/` convention. Public
pages such as `/`, `/login/`, and `/projects/` do not use this prefix.

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
Image originals are normalized to metadata-free JPEG at 90 percent quality and
constrained to 1500 pixels on each axis without upscaling. Previews are
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

Markdown post text is rendered client-side with `markdown-it`. Embedded raw
HTML is disabled; Markdown-generated markup is styled by the dedicated
`MarkdownContent` component.

The current router implements:

```text
/                Empty About page
/projects/        Projects loaded from the REST API
/projects/:project/ Project posts loaded from the REST API
/projects/:project/:postNumber/ Individual post loaded from the REST API
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
- `ProjectCard` for public and visually locked project states.
- `PostCardList` for presentation-only square cards with an optional caption
  and rating;
- `RatedPostHeader` for detail types whose title sits beside an overall rating.
- `PostRowList` for presentation-only rows with a media slot, label, and date;
- `DatedPostHeader` for text detail pages with an optional date;
- `MarkdownContent` for styled, HTML-disabled Markdown rendering.
- `PostTag` for non-interactive tag labels on post detail pages;
- `RelatedPostLink` for links to a post's optional same-project relation.
- `PostFileList` for non-image and non-video file links using original names.

Detail post responses expose `relatedPost` as an object containing its `number`
and model-generated `link`. The frontend uses that link directly and does not
reconstruct backend routes.

Projects are returned in ascending explicit project order. Posts within a
project are returned by descending post number, with the highest-numbered item
first.

The project-posts page fetches a project and its posts from the REST API, then
uses an explicit mapping from the project's `postListType` code to a component in
`components/post-list-types`. Each list component receives the project's
`posts` array and maps its type-specific fields into display data for either
`PostCardList` or `PostRowList`. The two base components contain only rendering
logic and do not inspect API post shapes. List entries contain only the fields
required by list components;
they do not expose `extra`, additional files, tags, or detail-page metadata.
List `mainFile` data includes the stored `mediaType` so presentation types can
distinguish photos, videos, audio, and other files without filename parsing.
Post dates come from the optional model field rather than `extra`. PostgreSQL
extracts only `rating` from `extra` for its dedicated list field. General post
lists use a dedicated summary serializer that returns a thumbnail and a label
derived from name, text excerpt, or file-type counts. Project posts use
page-number pagination with 50 posts per page;
the response includes the current page, page size, total pages, and total posts.
The frontend keeps the selected page in the URL query string and renders numeric
page controls.

The individual-post page selects its component through an explicit mapping from
the API's `postType` value. Concrete list and post presentation behavior is
specified in `docs/PROJECT_TYPES.md`.

Projects come from the REST API. Anonymous users never receive private projects;
authenticated guests receive them with `isPublic: false` so the existing locked
card presentation can distinguish them.

The login form uses Django session authentication with CSRF protection and
redirects successful logins to the project grid. The header action reflects the
current session and provides logout. The language switch stores its selection
only in component state and does not translate or persist content.

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
