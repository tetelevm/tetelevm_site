# tetelevm_site

tetelevm's personal website—a place to learn about the author, his interests,
and his creative work.

The main part of the website is dedicated to formats: themed collections of
texts, photographs, and other materials. Each format brings together posts
related by a common subject and may have its own form of presentation—from photo
galleries and short notes to detailed stories about travels, places, and
interests.

## Site export

Install the dependencies from `backend/requirements.txt`, then copy the script's
configuration template:

```bash
cp scripts/.env.example scripts/.env
chmod 600 scripts/.env
```

Edit `scripts/.env` and set `SITE_URL`, `TARGET`, `USERNAME`, `PASSWORD`, and
`PROJECTS` (comma-separated project slugs). All five settings are required.
The file is ignored by Git and excluded from Docker images.

```bash
python scripts/download_site.py
```

The script always loads `.env` beside itself, regardless of the current working
directory. A relative `TARGET` is resolved from the current working directory.
Values are read literally, without environment variable interpolation; quote
values containing spaces or an inline `#` comment marker. Process environment
variables do not override this configuration.
