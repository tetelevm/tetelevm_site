# Production deployment

One Debian/Ubuntu VPS runs Docker Compose, PostgreSQL, Gunicorn, and Caddy.
Install Docker Engine/Compose and Git, point the domain's DNS `A` record at the
server, and allow TCP 80/443 (optionally UDP 443 for HTTP/3). Keep SSH restricted;
database and Gunicorn ports must not be publicly exposed.

## First deployment

```bash
git clone <repository-url> tetelevm_site
cd tetelevm_site
cp .env.production.example .env.production
chmod 600 .env.production
openssl rand -base64 48
openssl rand -base64 36
```

Replace example credentials with independent secrets. `DOMAIN` and
`DJANGO_ALLOWED_HOSTS` take hostnames; `DJANGO_CSRF_TRUSTED_ORIGINS` takes the
full HTTPS origin, without a path or trailing slash. `GOOGLE_SITE_VERIFICATION`
is the Search Console token, not its complete HTML element.

```bash
mkdir -p media
docker compose -f compose.prod.yaml config --quiet
docker compose -f compose.prod.yaml up -d --build
docker compose -f compose.prod.yaml ps
docker compose -f compose.prod.yaml logs --tail=100 backend web
docker compose -f compose.prod.yaml exec backend python manage.py check --deploy
```

Caddy obtains TLS certificates once DNS and ports are reachable. Review Django's
checks: HSTS subdomain/preload warnings are expected with the example settings;
a weak secret warning must be fixed. Once HTTPS works, create the administrator:

```bash
docker compose -f compose.prod.yaml exec backend python manage.py createsuperuser
```

Check the home, archive, media, login/logout, and administration. Verify
anonymous, guest, and administrator visibility. Check exposed ports from another
machine; Docker port publishing can interact with host firewall rules.

## Updates and routine operation

Back up the database and media before changes to models or file handling.

```bash
git pull --ff-only
docker compose -f compose.prod.yaml up -d --build
docker compose -f compose.prod.yaml ps
docker compose -f compose.prod.yaml logs --tail=100 backend web
```

The backend applies migrations and collects static assets before Gunicorn starts.
Periodically check `df -h` and `docker system df`, install security updates, and
prune unused build cache only after confirming the deployment works. Services
use `restart: unless-stopped` and return after Docker starts.

Operator scripts are available under `/app/scripts` in the backend container:

```bash
docker compose -f compose.prod.yaml exec -T backend \
  sh -c 'python manage.py shell < /app/scripts/<script-name>.py'
```

## Backups and restore

Back up both database and uploaded media, keep dated copies off the VPS, and
test restoration. Treat backups as private data.

```bash
docker compose -f compose.prod.yaml exec -T db sh -c \
  'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB"' > tetelevm.sql
tar -czf tetelevm-media.tar.gz media
```

Restore into an empty database, on a separate server or an explicitly verified
target; restoration overwrites application data:

```bash
docker compose -f compose.prod.yaml up -d db
docker compose -f compose.prod.yaml exec -T db sh -c \
  'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"' < tetelevm.sql
```

Restore the media archive into the repository root before starting the full
stack. Preserve PostgreSQL/Caddy volumes and `media/` across container replacement.
