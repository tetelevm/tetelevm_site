# Agent Instructions

## Sources of truth

- `docs/BUSINESS.md` defines product behavior and user capabilities. Keep it
  implementation-agnostic.
- `docs/TECHNICAL.md` defines architecture and implementation decisions.
- `README.md` contains the repository overview and setup instructions.

Read the relevant documentation before changing behavior or architecture. When
behavior changes, update `docs/BUSINESS.md`; when implementation or architecture
changes materially, update `docs/TECHNICAL.md`.

## Engineering approach

This is a low-traffic personal site, not a generic CMS or high-load platform.
Prefer the smallest straightforward Django/Vue solution that satisfies the
documented requirement. Do not turn deferred decisions into permanent
architecture before a concrete feature requires them.

Do not add speculative infrastructure or product features. In particular, do
not introduce Redis, Celery, message brokers, Kubernetes, JWT, a custom
authentication framework, complex RBAC, per-item permissions, or a generic page
builder without an explicit requirement.

## Product and security invariants

- Use standard Django authentication with session cookies.
- Enforce authentication, project visibility, and content authorization on the
  backend. Frontend filtering is not a security boundary.
- Content inherits visibility from its project unless the business requirements
  explicitly change.
- Anonymous and guest access is read-only; Django Admin is the primary authoring
  interface.
- Do not expose Django's default login UI as the normal visitor login
  experience.
- Handle CSRF correctly for every state-changing request.

## Implementation boundaries

- Add type annotations to functions and methods. Use
  `from __future__ import annotations` where it keeps annotations simple.
- Docstrings are optional for straightforward functions and classes. Add them
  when they clarify complex or non-obvious logic.
- Keep the GraphQL schema driven by actual frontend screens and use cases.
- Keep mappings from project/content presentation types to Vue components
  explicit and maintainable.
- Treat data in `frontend/src/pages/ProjectsPage.vue` and the login error as
  temporary UI fixtures until backend integration replaces them.
- Preserve the shared header, project grid, and project card component
  boundaries unless a concrete design change requires restructuring them.
- Keep the user-facing interface usable on desktop and mobile.
- Store secrets and production credentials in environment configuration, never
  in the repository.

## Verification

Test behavior in proportion to its risk. Backend coverage should prioritize
authorization, authentication, GraphQL exposure, and domain invariants. Use
pytest with pytest-django unless there is a concrete reason to choose otherwise.

Do not consider authorization-sensitive work complete until anonymous, guest,
and administrator behavior has been checked where relevant.
