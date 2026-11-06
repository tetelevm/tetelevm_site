# Technical Architecture

## Stack and boundaries

A single-server Django/DRF, PostgreSQL, Vue 3, Vue Router, and Vite application.
Django owns persistence, authorization, domain rules, media, and administration;
Vue owns public routing and presentation. Django Admin is the authoring interface.
Frontend filtering is never an authorization boundary.

| Path | Responsibility |
| --- | --- |
| `backend/apps/core/` | Files, session API, profile, maintenance, HTTP examples. |
| `backend/apps/projects/` | Formats, posts, tags, administration, and read APIs. |
| `frontend/src/` | Pages, shared components, explicit presentation mappings. |
| `media/` | Persistent uploads, ignored by Git. |
| `deploy/`, `compose*.yaml` | Development and production containers. |
| `scripts/` | Export and operator maintenance routines, not application logic. |

Product rules are in [BUSINESS.md](BUSINESS.md), visual type specifications in
[PROJECT_TYPES.md](PROJECT_TYPES.md), and operating procedures in
[DEPLOYMENT.md](DEPLOYMENT.md).

## Authentication and authorization

Use standard Django users and session cookies: a shared non-staff guest account
and the owner's staff/superuser account. Login/logout use CSRF tokens obtained
from `/_api/auth/csrf/` and sent in `X-CSRFToken`. All state-changing requests,
including administrative maintenance, require CSRF protection.

Backend querysets restrict anonymous reads to public projects. Authenticated
guests can read private content but cannot write. Superuser-only export APIs
check permissions on the backend. The header loads the session to render its
login/logout and staff controls.

## Domain and administration

The public term is “format”; Python models remain `Project`/`project`.
A project owns visibility, lifecycle status, order, cover, and independent
`post_type` and `post_list_type` choices. Status does not affect authorization.

`Post` belongs to one project, has a unique number within it, optional text,
date/name/main file, JSON `extra`, tags, symmetric related posts, and additional
files ordered through `PostFile`. Model validation and a database constraint
require positive published numbers and non-positive draft numbers.
`PostQuerySet.published()` is used for lists, counts, filtering, random selection,
and navigation. Only staff detail/metadata reads may include drafts.

`PostFile` order uniqueness is deferred until transaction commit so existing
positions can be swapped in Admin. Preserve this when changing inline saves.
`Post.display_label` supplies shared labels; queryset annotations supply file
counts and nearest adjacent posts without per-item lookups. List serializers
expose card summaries instead of full post bodies/metadata. The format-post API
paginates by 48 and applies `tag` filtering before pagination.

`PostAdminForm` exposes validated typed fields for `extra`, enabling the subset
for the selected post type. Saves remove known fields of other types while
preserving unknown metadata; legacy anime `subtitle` is discarded.
File/post selectors use Django autocomplete. Administrative file labels are
independent of stored paths.

## Profile

`core.Profile` stores one JSON record per unique `ru`/`en` language, created
manually in Admin. `ProfileContentForm` defines the fixed schema and validates
image/PDF selections, HTTP(S) contact URLs, and plain email addresses;
`ProfileAdminForm` exposes editable content instead of raw JSON. Its three file
selectors reuse Django Admin file autocomplete and initially load only selected
options. Interface
captions and contact labels live in the frontend RU/EN dictionary in
`frontend/src/config/profile.js`.
The biography uses the shared `MarkdownContent` renderer with profile typography.

The public profile API resolves file IDs to URLs and email to `mailto:`.
The résumé URL points to `/_api/profile/<language>/resume/`, which streams only
that profile's selected PDF using Django `FileResponse` and an inline
`Content-Disposition` with the filename from `Profile.data.resumeFilename`
(UTF-8 for non-ASCII names), falling back to `resume.pdf` when empty or absent.
The profile form validates a plain PDF filename and exposes it in Admin;
the existing JSON field stores it without a schema migration.
The response is not cached; stored UUID paths are unchanged.
Missing files yield null URLs; absent/unsupported languages return 404.
It reads the database without caching. JSON references do not participate in
file deletion or orphan detection; service-post attachments retain these files.

## Routes

| Route | Purpose |
| --- | --- |
| `/`, `/login/` | Profile and visitor login. |
| `/archive/`, `/archive/<format>/`, `/archive/<format>/<n>/` | Formats and posts. |
| `/archive/random/` | Redirect to a visible starred post. |
| `/_api/profile/<language>/` | Localized profile. |
| `/_api/formats/`, `/_api/formats/<format>/`, `/_api/formats/<format>/<n>/` | Read APIs. |
| `/_api/random-post/` | Canonical link to a random visible published `star` post. |
| `/_api/auth/{csrf,session,login,logout}/` | Session API. |
| `/_api/page-meta/` | Server-rendered titles and social metadata for a path. |
| `/_api/tags/`, `/_api/files/<uuid>/`, `/_api/formats/<format>/post-tags/` | Superuser export metadata. |
| `/_admin/`, `/_static/`, `/files/` | Administration, Django static assets, media. |
| `/robots.txt`, `/sitemap.xml` | Search discovery. |
| `/r/<code>/` | Synthetic responses implemented in `core/http_status/`. |

`/formats/`, `/projects/`, and `/_api/projects/` remain compatibility aliases.
Unknown public URLs use the real 404 status. Caddy injects Django page metadata
into the frontend HTML; missing content triggers its 404 template, and drafts
visible to staff receive `noindex`. Metadata and sitemap queries must preserve
visibility restrictions.

## Media and maintenance

Files have UUID paths, editable labels, and extension-derived media types.
Originals live under `content/`, thumbnails under `thumbnail/`. Default image
processing applies EXIF orientation, strips metadata, and creates a JPEG original
bounded to 1500px plus a centered 150px square JPEG thumbnail. Bulk upload can
preserve original bytes; GIF originals always retain their bytes and animation.
`link`/`link_full` point to originals; `link_small` prefers the thumbnail.
Detail media uses originals, not separate medium-sized previews.

`find_orphan_files` finds records unused as covers, main files, or attachments,
including drafts. `tidy_media` deletes physical files with no `File.content` or
`File.thumbnail` reference, retaining database records and `.gitkeep`.
`relabel_project_files` assigns format/number/position labels without changing
paths, processing main files first; shared files take the last processed label.
Mutating maintenance views require a staff superuser, confirmation, and POST.

## Frontend

`MainLayout`, `AppHeader`, and `AppFooter` provide the shared shell and centered
800px content area. `ProjectGrid`/`ProjectCard` own format cards. Keep these
boundaries unless a concrete design change requires restructuring them.
`config/postTypes.js` explicitly maps list/detail type codes to components.
Detail types compose shared post layout/header/footer and media blocks;
list adapters supply data to reusable card/row components.

`MarkdownContent` uses `markdown-it` with raw HTML disabled and supports native
collapsible spoilers. Embedded media is selected by URL extension; links and
captions are escaped. `MediaFile`, `MediaCarousel`, and the shared lightbox
handle structured attachments. Images preserve aspect ratio; a carousel retains
its current size until the next image loads.

The profile page fetches the selected language and aborts superseded requests.
Profile components receive content via props; `config/profile.js` defines
the contact layout and localized interface text. `ProfileIntro` uses a grid with
a 3:5 portrait and a text column above 600px, stacking the portrait above the
text on smaller screens. The `before-footer` slot holds the credit.
Language selection is page-local.
Global CSS supplies the dark/lime palette and bundled Sofia Sans/IBM Plex Mono.
Contact icons use Iconify Vue with bundled Remix Icon and Simple Icons SVG data.

## Development, production, and verification

`compose.yaml` runs Vite, Django's development server, and PostgreSQL. Vite
proxies API and media requests. Its dependency volume is refreshed by `npm install`
on startup. `compose.prod.yaml` runs PostgreSQL, Gunicorn (one worker, two threads),
and Caddy. Only Caddy exposes public ports; it serves built Vue, media, static
assets, TLS, and backend proxies. Migrations and static collection run before
Gunicorn starts. Database/static/Caddy state use volumes; uploads use `media/`.
Secrets belong in environment files excluded from Git. See [DEPLOYMENT.md](DEPLOYMENT.md).

Backend tests use pytest with pytest-django, including existing Django TestCases.
Prioritize authorization, sessions/CSRF, draft visibility, domain invariants,
file preservation, and destructive maintenance. Avoid exhaustive checks of
cosmetic HTML, simple framework behavior, and the HTTP joke playground.
Frontend verification uses `npm run build`.

The export client `scripts/download_site.py` uses a CSRF-protected session and
superuser metadata APIs; setup is in [README.md](../README.md#site-export).
Explicit saver mappings produce per-format exports. `info/saved_posts.txt`
tracks incremental progress; removing a number forces its re-export.
Operator helpers are copied into `/app/scripts` in the backend image.

Keep the architecture proportional to a personal site: no Redis, Celery, JWT,
complex RBAC, page builder, or orchestration platform without a concrete need.
