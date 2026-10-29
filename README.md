# tetelevm_site

tetelevm's personal website—a place to learn about the author, his interests,
and his creative work.

The main part of the website is dedicated to formats: themed collections of
texts, photographs, and other materials. Each format brings together posts
related by a common subject and may have its own form of presentation—from photo
galleries and short notes to detailed stories about travels, places, and
interests.

## Site export

Configure the URL, destination, and projects at the top of
`scripts/download_site.py`. Supply credentials through `SITE_DOWNLOAD_USERNAME`
and `SITE_DOWNLOAD_PASSWORD` environment variables; do not put them in the script.
For an interactive Bash session, read them without saving their values in shell
history:

```bash
read -r -p 'Username: ' SITE_DOWNLOAD_USERNAME
read -r -s -p 'Password: ' SITE_DOWNLOAD_PASSWORD
printf '\n'
export SITE_DOWNLOAD_USERNAME SITE_DOWNLOAD_PASSWORD
python scripts/download_site.py
unset SITE_DOWNLOAD_USERNAME SITE_DOWNLOAD_PASSWORD
```

The script reads the process environment directly; it does not load `.env` files.
