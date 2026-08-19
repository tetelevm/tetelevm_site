# tetelevm_site

Personal website built with Django REST Framework and Vue.

The first frontend prototype is complete. It includes a responsive Projects
page, an About-page construction notice, session login, and backend-driven
project pages.

## Start development

Copy the environment template once:

```bash
cp .env.example .env
```

Build and start all services:

```bash
docker compose up --build
```

Run them in the background with `-d`. Stop them with:

```bash
docker compose down
```

Development URLs:

- frontend: http://localhost:5173;
- Django: http://localhost:8000;
- Django Admin: http://localhost:8000/_admin/;
- REST API: http://localhost:8000/_api/.

The frontend container runs `npm install` on startup so its persistent
`node_modules` volume stays synchronized with `package-lock.json`.

## Current frontend

Implemented Vue routes:

- `/` — localized About-page construction notice, navigation, and footer with
  a non-persistent `ru/en` UI switch;
- `/projects/` — responsive project card grid loaded from the REST API;
- `/login/` — session login form for guests and administrators.

The Projects page dims private project cards without labeling their visibility.
Paused projects carry a warm “на паузе” badge and closed projects a red
“завершён” badge; open projects have no status badge. Each card shows its post
total on the bottom-left of the cover. The backend omits private projects
entirely for anonymous users. The page uses reusable header, language switch,
login link, grid, and card components. The favicon is served from
`frontend/public/favicon.ico`.

The following frontend behavior is intentionally not implemented yet:
- persistent language selection or translated project content;
- project list and item detail pages;
- real project images and backend media.

## Verification

Build the frontend and audit its dependencies with:

```bash
cd frontend
npm run build
npm audit --audit-level=high
```

## Documentation

- `docs/BUSINESS.md` defines product behavior and user capabilities.
- `docs/TECHNICAL.md` describes current state and intended architecture.
- `docs/PROJECT_TYPES.md` describes the visual presentation of project types.
- `docs/DEPLOYMENT.md` describes production deployment and maintenance.
- `AGENTS.md` contains repository instructions for coding agents.
