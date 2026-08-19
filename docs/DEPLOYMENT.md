# Production deployment

This deployment targets one low-traffic Debian or Ubuntu VPS with a public IP.
It uses Docker Compose, PostgreSQL, Gunicorn, and Caddy. Caddy automatically
obtains and renews the HTTPS certificate.

## Before deployment

The server must have:

- Docker Engine with the Compose plugin;
- Git;
- inbound TCP ports 80 and 443 open;
- inbound UDP port 443 open for HTTP/3 (optional, but supported by the Compose
  file);
- an inbound SSH port restricted as appropriate;
- a DNS `A` record pointing the chosen hostname to the server's public IPv4.

Do not publish the database or Gunicorn ports. Docker-published ports can
interact unexpectedly with host firewall rules, so verify the effective rules
from another machine.

## First deployment

Clone the repository and enter it:

```bash
git clone <repository-url> tetelevm_site
cd tetelevm_site
```

Create the production environment file:

```bash
cp .env.production.example .env.production
chmod 600 .env.production
```

Generate independent secrets:

```bash
openssl rand -base64 48
openssl rand -base64 36
```

Edit `.env.production` and replace every example value. `DOMAIN` and
`DJANGO_ALLOWED_HOSTS` contain a hostname such as `example.com`, while
`DJANGO_CSRF_TRUSTED_ORIGINS` contains the complete HTTPS origin such as
`https://example.com`. Do not add URL paths or trailing slashes.

Ensure the persistent media directory exists, then build and start the stack:

```bash
mkdir -p media
docker compose -f compose.prod.yaml config --quiet
docker compose -f compose.prod.yaml up -d --build
```

Inspect container state and startup logs:

```bash
docker compose -f compose.prod.yaml ps
docker compose -f compose.prod.yaml logs --tail=100 backend web
```

Caddy can obtain a certificate only after DNS points to the server and ports 80
and 443 are reachable. DNS propagation can delay the first successful attempt;
Caddy retries automatically.

Run Django's production checks:

```bash
docker compose -f compose.prod.yaml exec backend python manage.py check --deploy
```

Review every warning. Create the administrator only after HTTPS works:

The example deliberately does not enable HSTS for every subdomain or browser
preloading, so Django reports those two advisory warnings. Enabling either is a
domain-wide commitment and is unnecessary for this small deployment. A weak
secret warning means `DJANGO_SECRET_KEY` was not replaced correctly and must be
fixed.

```bash
docker compose -f compose.prod.yaml exec backend python manage.py createsuperuser
```

Verify the public page, `/projects/`, `/_admin/`, login/logout, and media loading.
Also verify anonymous, guest, and administrator visibility.

## Deploying an update

Back up the database and media before an update that changes models or file
handling. Then fetch the reviewed code and rebuild:

```bash
git pull --ff-only
docker compose -f compose.prod.yaml up -d --build
docker compose -f compose.prod.yaml ps
docker compose -f compose.prod.yaml logs --tail=100 backend web
```

The backend applies migrations and collects Django static files before Gunicorn
starts. With one backend container this keeps the release procedure simple.

Remove unused build cache occasionally, after confirming the current deployment
works:

```bash
docker builder prune
```

## Backups

A useful backup must leave the VPS. Server snapshots are helpful but are not a
replacement for independent database and media copies.

Create a PostgreSQL dump:

```bash
docker compose -f compose.prod.yaml exec -T db sh -c \
  'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB"' > tetelevm.sql
```

Archive uploaded media:

```bash
tar -czf tetelevm-media.tar.gz media
```

Copy both files to another machine or backup service. Protect them as private
data. Keep more than one dated generation and periodically test restoration.

To restore into an empty database, start the database first and pass the dump to
`psql`:

```bash
docker compose -f compose.prod.yaml up -d db
docker compose -f compose.prod.yaml exec -T db sh -c \
  'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"' < tetelevm.sql
```

Restore the media archive into the repository root before starting the complete
stack. Restoration overwrites application data and therefore should be tested
on a separate server or after explicitly confirming the target.

## Routine checks

Occasionally check disk usage and service state:

```bash
df -h
docker system df
docker compose -f compose.prod.yaml ps
```

Install Debian security updates regularly. Reboot when required; all services
use `restart: unless-stopped` and return after Docker starts.
