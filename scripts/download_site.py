from __future__ import annotations

import filecmp
import json
import shutil
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlsplit
from urllib.request import HTTPCookieProcessor, Request, build_opener

from PIL import Image, ImageOps


SITE_URL = "https://example.com"
TARGET = Path("./site_export")
USERNAME = ""
PASSWORD = ""
PROJECTS = [
    "project-slug",
]


class SiteDownloader:
    def __init__(self, site_url: str, target: Path) -> None:
        self.site_url = site_url.rstrip("/")
        self.target = target
        self.opener = build_opener(HTTPCookieProcessor(CookieJar()))

    def _get_json(
        self, path: str, data: dict[str, str] | None = None, csrf_token: str = ""
    ) -> dict[str, Any]:
        headers = {"Accept": "application/json"}
        body = None
        if data is not None:
            headers.update({
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token,
                "Origin": self.site_url,
            })
            body = json.dumps(data).encode("utf-8")

        request = Request(self.site_url + path, data=body, headers=headers)
        with self.opener.open(request, timeout=30) as response:
            return json.load(response)

    def _login(self, username: str, password: str) -> None:
        token = self._get_json("/_api/auth/csrf/")["csrfToken"]
        session = self._get_json(
            "/_api/auth/login/",
            {"username": username, "password": password},
            token,
        )
        if not session["isAuthenticated"]:
            raise RuntimeError("Не удалось войти на сайт")

    def _save_cover(self, cover_url: str, directory: Path) -> None:
        url = urljoin(self.site_url + "/", cover_url)
        with self.opener.open(url, timeout=30) as response:
            with Image.open(response) as source:
                image = ImageOps.exif_transpose(source).convert("RGBA")
                background = Image.new("RGB", image.size, "white")
                background.paste(image, mask=image.getchannel("A"))
                background.save(directory / "main.jpg", format="JPEG", quality=90)

    def _init_project(self, slug: str, cover_url: str) -> Path:
        directory = self.target / slug
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "images").mkdir(exist_ok=True)
        info = directory / "info"
        info.mkdir(exist_ok=True)
        self._save_cover(cover_url, directory)
        (info / "saved_posts.txt").touch(exist_ok=True)
        return directory

    def save_tags(self) -> None:
        tags = self._get_json("/_api/tags/")
        self.target.mkdir(parents=True, exist_ok=True)
        (self.target / "tags.json").write_text(
            json.dumps(tags, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _save_post_content(
        self, post: dict[str, Any], directory: Path, slug: str
    ) -> list[dict[str, Any]]:
        savers = {
            "leksebi": self.save_leksebi,
            "gancdebi": self.save_gancdebi,
            "ikhvomedia": self.save_ikhvomedia,
        }
        saver = savers.get(slug)
        if saver:
            return saver(post, directory)
        path = directory / f"{post['number']}.json"
        path.write_text(
            json.dumps(post, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        # TODO: добавить обработчики остальных форматов и их медиа.
        return []

    def _save_related_posts(
        self, post: dict[str, Any], path: Path, related: dict[str, list[str]]
    ) -> None:
        number = str(post["number"])
        links = []
        for item in post["relatedPosts"]:
            parts = urlsplit(item["link"]).path.strip("/").split("/")
            links.append(f"{parts[-2]}/{parts[-1]}")
        related[number] = links
        path.write_text(
            json.dumps(related, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _download_file(
        self, file: dict[str, Any], directory: Path, replace_existing: bool = False
    ) -> str:
        metadata = self._get_json(f"/_api/files/{file['id']}/")
        name = metadata["label"] or file["name"]
        if not name or name in {".", ".."} or Path(name).name != name:
            raise ValueError(f"Некорректное имя файла: {name!r}")

        path = directory / "images" / name
        temporary = path.with_name(path.name + ".part")
        url = urljoin(self.site_url + "/", file["linkFull"])
        try:
            with self.opener.open(url, timeout=30) as response:
                with temporary.open("wb") as output:
                    shutil.copyfileobj(response, output)
            if path.exists() and not replace_existing:
                if not filecmp.cmp(path, temporary, shallow=False):
                    raise ValueError(f"Разные файлы имеют одно имя: {name}")
            else:
                temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)
        return name

    def _save_files(
        self,
        post: dict[str, Any],
        directory: Path,
        path: Path,
        photos: dict[str, dict[str, Any]],
        extra_files: list[dict[str, Any]],
        replace_existing: bool,
    ) -> None:
        main_file = post["mainFile"]
        main = (
            self._download_file(main_file, directory, replace_existing)
            if main_file else None
        )
        files = [
            self._download_file(file, directory, replace_existing)
            for file in [*post["files"], *extra_files]
        ]
        photos[str(post["number"])] = {"main": main, "files": files}
        path.write_text(
            json.dumps(photos, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def save_post(
        self,
        slug: str,
        post_number: str,
        directory: Path,
        saved_numbers: set[str],
        related: dict[str, list[str]],
        photos: dict[str, dict[str, Any]],
    ) -> int:
        is_saved = post_number in saved_numbers
        if is_saved and post_number in related and post_number in photos:
            return 0

        action = "Обновляю связи и файлы" if is_saved else "Скачиваю пост"
        print(f"  {action} #{post_number}", flush=True)
        post = self._get_json(f"/_api/formats/{slug}/{post_number}/")
        info = directory / "info"
        extra_files = (
            self._save_post_content(post, directory, slug)
            if not is_saved or post_number not in photos else []
        )
        if not is_saved or post_number not in related:
            self._save_related_posts(post, info / "related.json", related)
        if not is_saved or post_number not in photos:
            self._save_files(
                post, directory, info / "photos.json", photos,
                extra_files, replace_existing=not is_saved,
            )
        if is_saved:
            return 0

        with (info / "saved_posts.txt").open("a", encoding="utf-8") as saved_posts:
            saved_posts.write(f"{post_number}\n")
        saved_numbers.add(post_number)
        return 1

    def download_project(self, slug: str) -> int:
        post_tags = self._get_json(f"/_api/formats/{slug}/post-tags/")
        project = self._get_json(f"/_api/formats/{slug}/")
        directory = self._init_project(slug, project["cover"])
        info = directory / "info"
        (info / "tag_list.json").write_text(
            json.dumps(post_tags, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        saved_posts_file = info / "saved_posts.txt"
        saved_numbers = set(saved_posts_file.read_text(encoding="utf-8").splitlines())
        related_path = info / "related.json"
        related = (
            json.loads(related_path.read_text(encoding="utf-8"))
            if related_path.exists() else {}
        )
        photos_path = info / "photos.json"
        photos = (
            json.loads(photos_path.read_text(encoding="utf-8"))
            if photos_path.exists() else {}
        )
        count = 0
        for number in sorted(post_tags, key=int):
            count += self.save_post(
                slug, number, directory, saved_numbers, related, photos
            )

        print(f"{slug}: скачано новых постов: {count}")
        return count

    def run(self, username: str, password: str, projects: list[str]) -> None:
        print("Логинюсь...", flush=True)
        self._login(username, password)
        print("Скачиваю список тегов...", flush=True)
        self.save_tags()
        for slug in projects:
            print(f"Скачиваю проект: {slug}", flush=True)
            self.download_project(slug)

    # === projects funcs ===

    def save_leksebi(
        self, post: dict[str, Any], directory: Path
    ) -> list[dict[str, Any]]:
        text = post["text"].rstrip("\n")
        if post["date"]:
            text += f"\n\n{post['date']}"
        (directory / f"{post['number']}.txt").write_text(text + "\n", encoding="utf-8")
        return []

    def save_gancdebi(
        self, post: dict[str, Any], directory: Path
    ) -> list[dict[str, Any]]:
        title = post["name"]
        if not title or Path(title).name != title:
            raise ValueError(f"Название нельзя использовать как имя файла: {title!r}")
        body = post["text"].rstrip("\n")
        (directory / f"{title}.txt").write_text(
            f"{post['date']}\n\n{body}\n", encoding="utf-8"
        )
        return []

    def save_ikhvomedia(
        self, post: dict[str, Any], directory: Path
    ) -> list[dict[str, Any]]:
        body = post["text"].rstrip("\n")
        text = f"# {post['name']}\n{post['date']}\n\n{body}\n"
        (directory / f"{post['number']}.txt").write_text(text, encoding="utf-8")
        return []


if __name__ == "__main__":
    SiteDownloader(SITE_URL, TARGET).run(USERNAME, PASSWORD, PROJECTS)
