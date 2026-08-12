# Technical Architecture

## Scope and status

The repository currently contains a working development foundation: Django,
Graphene, Vue, Vite, PostgreSQL, and Docker Compose. The frontend includes a
static Projects page prototype built from reusable navigation, grid, and card
components. Separate Vue routes exist for About, Projects, and Login. Domain
models, API integration, authentication, media handling, tests, and production
deployment are still to be implemented.

This document describes the intended architecture. A capability mentioned here
should not be treated as already implemented unless it exists in the codebase.

## Repository layout

```text
/
├── backend/       Django, GraphQL, administration, and backend tests
├── frontend/      Vue application and frontend tests
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
through GraphQL.

Django is responsible for:

- persistence and domain rules;
- authentication state and authorization;
- project and content visibility;
- administrative content management;
- media metadata and file handling;
- exposing safe data through GraphQL.

Vue is responsible for:

- public routing and presentation;
- the custom guest login experience;
- responsive desktop and mobile layouts;
- rendering projects and items according to their presentation type.

Frontend filtering is presentation logic, not a security boundary.

## Backend

The backend uses Python, Django, Graphene, PostgreSQL, and Django Admin.

Django Admin is the primary authoring interface. A broad set of administrative
GraphQL mutations is therefore unnecessary. The GraphQL schema should remain
small and be expanded in response to actual frontend use cases.

Expected read capabilities include:

- current authentication state when needed by the interface;
- projects visible to the current user;
- details and items for a selected project;
- individual item details when required by a project type.

GraphiQL may be enabled in development but must remain disabled when Django is
not running in debug mode.

## Authentication and authorization

Use Django's standard user and session authentication. The initial account model
contains:

- anonymous visitors with access to public content;
- one non-staff shared guest account with access to private content;
- the site owner's staff or superuser account for administration.

Do not introduce JWT or a custom authentication framework without a client or
deployment requirement that makes session authentication unsuitable.

Authorization must be enforced in backend query resolution. Anonymous GraphQL
requests must not reveal private projects or items belonging to them.

CSRF protection is required for login, logout, and every state-changing
operation. The current GraphQL endpoint is a read-only scaffold and is CSRF
exempt; that exemption must be removed or narrowed before adding mutations or
other session-authenticated writes.

## Content domain

The stable conceptual model is:

```text
Project
    visibility: public | private
    presentation_type

ContentItem
    project -> Project
```

A project is an independent content collection. It owns the visibility and
presentation context inherited by its items. A content item belongs to exactly
one project and contains the material required by that project's presentation.

The exact model fields and the storage strategy for heterogeneous content are
intentionally deferred until the first concrete project types are designed.
Avoid a generic page builder or universal CMS schema without a demonstrated
need.

The backend should expose an explicit presentation type. The frontend should
map that type to a known Vue component. Keep this mapping simple and visible in
the codebase.

## User-facing routes

The intended routes are:

```text
/                               About
/login/                         Guest login
/content/                       Projects visible to the visitor
/content/<project>/             Items in a project
/content/<project>/<item>/      Item detail when the project needs one
```

Exact identifiers and slug behavior remain deferred. The Content landing page
must remain project-oriented rather than becoming a global mixed feed.

## Internal routes

Internal and operational HTTP routes use an underscore prefix to distinguish
them from the public site structure. Current routes are:

```text
/_admin/                       Django Admin
/_graphql/                     GraphQL API and development GraphiQL
/_static/                      Django-managed static assets
```

Future internal endpoints should follow the same `/_name/` convention. Public
pages such as `/`, `/login/`, and `/content/` do not use this prefix.

## Media

Initial uploads are managed through Django Admin and stored on persistent VPS
storage. Production deployment must preserve uploaded files independently of
container replacement.

External embeds or media providers may be added when a concrete content type
requires them. They are not part of the initial infrastructure.

## Frontend

The frontend uses Vue, Vue Router, and Vite. Public pages, including login,
belong to Vue. Different project types may use different components, but the
application should not become a runtime page-builder.

Frontend testing should be proportional to the amount of meaningful client-side
logic. Static presentation does not require exhaustive component tests.

## Testing

Use pytest and pytest-django for backend tests unless a concrete constraint
requires another tool. Prioritize behavior with security or domain significance:

- anonymous users cannot retrieve private projects or their items;
- guests can retrieve private projects and remain read-only;
- guest users cannot obtain staff or administrative capabilities;
- visibility is applied consistently to every item in a project;
- GraphQL resolvers enforce authorization;
- login, logout, and session behavior work correctly;
- core model invariants are preserved.

## Development and deployment

Local development uses the root `compose.yaml` with three services:

- `frontend` for the Vite development server;
- `backend` for the Django development server;
- `db` for PostgreSQL.

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

- exact Django model fields and GraphQL naming;
- concrete project and item presentation types;
- storage for heterogeneous item content;
- detailed visual design and SEO strategy;
- external media and embed support;
- production application server and reverse proxy;
- backup and deployment procedures;
- which About-page fields, if any, should be editable.
