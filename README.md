# tetelevm_site

Personal website built with Django REST Framework and Vue.

The first frontend prototype is complete. It includes a responsive Projects
page, an empty About page, and a guest login form. Backend domain logic and
frontend-to-backend integration are the next development stage.

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

- `/` — empty About page with a non-persistent `ru/en` UI switch;
- `/content/` — responsive project card grid using temporary local data;
- `/login/` — login form UI with a temporary simulated error state.

The Projects page supports ordinary and visually private project cards. Private
examples currently exist only as design fixtures; the backend will omit them
entirely for anonymous users. The page uses reusable header, language switch,
login link, grid, and card components. The favicon is served from
`frontend/public/favicon.ico`.

The following frontend behavior is intentionally not implemented yet:

- loading the project grid from the REST API;
- real login, logout, and session state;
- persistent localization or translated content;
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
- `AGENTS.md` contains repository instructions for coding agents.
