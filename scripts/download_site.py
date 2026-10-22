from __future__ import annotations

import filecmp
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Self
from urllib.parse import quote, unquote, urljoin, urlsplit

import requests
from PIL import Image, ImageOps


SITE_URL = "https://example.com"
TARGET = Path("./site_export")
USERNAME = ""
PASSWORD = ""
PROJECTS = [
    "project-slug",
]


@dataclass(frozen=True)
class SavedFile:
    name: str
    media_type: str
    source_urls: tuple[str, ...] = ()

    def markdown_image(self) -> str:
        return f"![](images/{quote(self.name, safe='')})"


@dataclass(frozen=True)
class SavedMedia:
    main: SavedFile | None
    files: list[SavedFile]
    site_url: str = ""
    public_files: list[SavedFile] | None = None

    def photos(self) -> list[SavedFile]:
        return [file for file in self.files if file.media_type == "photo"]

    def attached_files(self) -> list[SavedFile]:
        return self.public_files if self.public_files is not None else self.files


class PostSaver:
    @classmethod
    def from_post(cls, post: dict[str, Any], media: SavedMedia) -> Self:
        raise NotImplementedError

    @classmethod
    def extra_post_numbers(cls, post: dict[str, Any]) -> list[int]:
        return []

    def write(self, directory: Path) -> None:
        raise NotImplementedError


INLINE_IMAGE = re.compile(
    r"(?P<prefix>!\[(?:\\.|[^\]])*\]\()(?P<url><[^>\n]+>|[^\s)]+)"
)


def localize_markdown_images(text: str, media: SavedMedia) -> str:
    files_by_path = {
        unquote(urlsplit(url).path): file
        for file in ([media.main] if media.main else []) + media.files
        for url in file.source_urls
    }
    site_host = urlsplit(media.site_url).netloc

    def replace(match: re.Match[str]) -> str:
        source = match.group("url")
        url = source[1:-1] if source.startswith("<") else source
        parsed = urlsplit(url)
        if parsed.scheme and parsed.scheme not in {"http", "https"}:
            return match.group(0)
        path = unquote(urlsplit(urljoin(media.site_url + "/", url)).path)
        file = files_by_path.get(path)
        if file is None and parsed.netloc and parsed.netloc != site_host:
            return match.group(0)
        if file is None:
            raise ValueError(f"Нет прикреплённого файла для Markdown-ссылки: {url}")
        return match.group("prefix") + f"images/{quote(file.name, safe='')}"

    return INLINE_IMAGE.sub(replace, text)


def linked_image_names(text: str) -> set[str]:
    names = set()
    for match in INLINE_IMAGE.finditer(text):
        path = Path(unquote(urlsplit(match.group("url").strip("<>")).path))
        if path.parent == Path("images"):
            names.add(path.name)
    return names


@dataclass
class CombinedMarkdown:
    directory: Path

    def save(self, number: str, content: str, filename: str = "posts.md") -> None:
        entries_path = self.directory / "info" / "combined_entries.json"
        entries = (
            json.loads(entries_path.read_text(encoding="utf-8"))
            if entries_path.exists() else {}
        )
        entries[str(number)] = content
        entries_path.write_text(
            json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (self.directory / filename).write_text(
            "\n\n".join(entries[key] for key in sorted(entries, key=int)) + "\n",
            encoding="utf-8",
        )


@dataclass
class YearlyMarkdown:
    directory: Path

    def save(
        self, number: str, year: str, content: str, filename: str | None = None
    ) -> None:
        entries_path = self.directory / "info" / "year_entries.json"
        entries = (
            json.loads(entries_path.read_text(encoding="utf-8"))
            if entries_path.exists() else {}
        )
        old_year = entries.get(str(number), {}).get("year")
        entries[str(number)] = {"year": year, "content": content}
        entries_path.write_text(
            json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        for affected_year in {year, old_year} - {None}:
            sections = [
                entries[key]["content"] for key in sorted(entries, key=int)
                if entries[key]["year"] == affected_year
            ]
            path = self.directory / (
                filename if affected_year == year and filename else f"{affected_year}.md"
            )
            if sections:
                path.write_text("\n\n".join(sections) + "\n", encoding="utf-8")
            else:
                path.unlink(missing_ok=True)


@dataclass
class RawJsonSaver(PostSaver):
    number: str
    post: dict[str, Any]

    @classmethod
    def from_post(cls, post: dict[str, Any], media: SavedMedia) -> Self:
        return cls(str(post["number"]), post)

    @property
    def file(self) -> str:
        return f"{self.number}.json"

    @property
    def text(self) -> str:
        return json.dumps(self.post, ensure_ascii=False, indent=2)

    def write(self, directory: Path) -> None:
        (directory / self.file).write_text(self.text + "\n", encoding="utf-8")


@dataclass
class LeksebiSaver(PostSaver):
    number: str
    body: str
    date: str | None

    @classmethod
    def from_post(cls, post: dict[str, Any], media: SavedMedia) -> Self:
        return cls(str(post["number"]), post["text"].rstrip("\n"), post["date"])

    @property
    def file(self) -> str:
        return f"{self.number}.txt"

    @property
    def text(self) -> str:
        return self.body + (f"\n\n{self.date}" if self.date else "")

    def write(self, directory: Path) -> None:
        (directory / self.file).write_text(self.text + "\n", encoding="utf-8")


@dataclass
class GancdebiSaver(PostSaver):
    number: str
    body: str
    date: str | None

    @classmethod
    def from_post(cls, post: dict[str, Any], media: SavedMedia) -> Self:
        return cls(str(post["number"]), post["text"].rstrip("\n"), post["date"])

    @property
    def file(self) -> str:
        return f"{self.number}.txt"

    @property
    def text(self) -> str:
        return f"{self.date}\n\n{self.body}"

    def write(self, directory: Path) -> None:
        (directory / self.file).write_text(self.text + "\n", encoding="utf-8")


@dataclass
class IkhvomediaSaver(PostSaver):
    number: str
    name: str
    body: str
    date: str | None

    @classmethod
    def from_post(cls, post: dict[str, Any], media: SavedMedia) -> Self:
        return cls(
            str(post["number"]), post["name"], post["text"].rstrip("\n"),
            post["date"],
        )

    @property
    def file(self) -> str:
        return f"{self.number}.txt"

    @property
    def text(self) -> str:
        return f"# {self.name}\n{self.date}\n\n{self.body}"

    def write(self, directory: Path) -> None:
        (directory / self.file).write_text(self.text + "\n", encoding="utf-8")


@dataclass
class NacherchebiSaver(PostSaver):
    number: str
    body: str
    date: str | None

    @classmethod
    def from_post(cls, post: dict[str, Any], media: SavedMedia) -> Self:
        return cls(str(post["number"]), post["text"].rstrip("\n"), post["date"])

    @property
    def file(self) -> str:
        return f"{self.number}.txt"

    @property
    def text(self) -> str:
        return f"{self.date}\n\n{self.body}"

    def write(self, directory: Path) -> None:
        (directory / self.file).write_text(self.text + "\n", encoding="utf-8")


@dataclass
class NatserebiSaver(PostSaver):
    number: str
    name: str
    body: str
    date: str | None
    main: SavedFile

    @classmethod
    def from_post(cls, post: dict[str, Any], media: SavedMedia) -> Self:
        if media.main is None:
            raise ValueError(f"У поста #{post['number']} нет главной фотографии")
        return cls(
            str(post["number"]), post["name"], post["text"].rstrip("\n"),
            post["date"], media.main,
        )

    @property
    def file(self) -> str:
        return f"{self.number}.md"

    @property
    def text(self) -> str:
        return (
            f"# {self.name}\n\n{self.body}\n\n_{self.date}_"
            f"\n\n{self.main.markdown_image()}"
        )

    def write(self, directory: Path) -> None:
        (directory / self.file).write_text(self.text + "\n", encoding="utf-8")


@dataclass
class NomrebiSaver(PostSaver):
    number: str
    date: str | None
    main: SavedFile

    @classmethod
    def from_post(cls, post: dict[str, Any], media: SavedMedia) -> Self:
        if media.main is None:
            raise ValueError(f"У поста #{post['number']} нет главной фотографии")
        return cls(str(post["number"]), post["date"], media.main)

    @property
    def file(self) -> str:
        return "posts.md"

    @property
    def text(self) -> str:
        parts = ["---", f"# {self.number}"]
        if self.date:
            parts.append(f"_{self.date}_")
        parts.append(self.main.markdown_image())
        return "\n\n".join(parts)

    def write(self, directory: Path) -> None:
        CombinedMarkdown(directory).save(self.number, self.text, self.file)


@dataclass
class NakhalebiSaver(PostSaver):
    number: str
    date: str | None
    main: SavedFile

    @classmethod
    def from_post(cls, post: dict[str, Any], media: SavedMedia) -> Self:
        if media.main is None:
            raise ValueError(f"У поста #{post['number']} нет главной фотографии")
        return cls(str(post["number"]), post["date"], media.main)

    @property
    def file(self) -> str:
        return "posts.md"

    @property
    def text(self) -> str:
        parts = ["---", f"_{self.number}_"]
        if self.date:
            parts.append(f"_{self.date}_")
        parts.append(self.main.markdown_image())
        return "\n\n".join(parts)

    def write(self, directory: Path) -> None:
        CombinedMarkdown(directory).save(self.number, self.text, self.file)


@dataclass
class SakhlugebaSaver(PostSaver):
    number: str
    main: SavedFile

    @classmethod
    def from_post(cls, post: dict[str, Any], media: SavedMedia) -> Self:
        if media.main is None:
            raise ValueError(f"У поста #{post['number']} нет главной фотографии")
        return cls(str(post["number"]), media.main)

    @property
    def file(self) -> str:
        return "posts.md"

    @property
    def text(self) -> str:
        return f"---\n\n_{self.number}_\n\n{self.main.markdown_image()}"

    def write(self, directory: Path) -> None:
        CombinedMarkdown(directory).save(self.number, self.text, self.file)


@dataclass
class KarebiSaver(PostSaver):
    number: str
    body: str
    main: SavedFile

    @classmethod
    def from_post(cls, post: dict[str, Any], media: SavedMedia) -> Self:
        if media.main is None:
            raise ValueError(f"У поста #{post['number']} нет главной фотографии")
        return cls(str(post["number"]), post["text"].rstrip("\n"), media.main)

    @property
    def file(self) -> str:
        return "posts.md"

    @property
    def text(self) -> str:
        parts = ["---", f"_{self.number}_", self.main.markdown_image()]
        if self.body:
            parts.append(self.body)
        return "\n\n".join(parts)

    def write(self, directory: Path) -> None:
        CombinedMarkdown(directory).save(self.number, self.text, self.file)


@dataclass
class NadzerpiSaver(PostSaver):
    number: str
    date: str | None
    main: SavedFile
    photos: list[SavedFile]

    @classmethod
    def from_post(cls, post: dict[str, Any], media: SavedMedia) -> Self:
        if media.main is None:
            raise ValueError(f"У поста #{post['number']} нет главной фотографии")
        return cls(str(post["number"]), post["date"], media.main, media.photos())

    @property
    def file(self) -> str:
        return f"{self.number}.md"

    @property
    def text(self) -> str:
        parts = []
        if self.date:
            parts.append(f"_{self.date}_")
        parts.extend([self.main.markdown_image(), "---"])
        parts.extend(file.markdown_image() for file in self.photos)
        return "\n\n".join(parts)

    def write(self, directory: Path) -> None:
        (directory / self.file).write_text(self.text + "\n", encoding="utf-8")


@dataclass
class MokhetialeSaver(PostSaver):
    number: str
    date: str | None
    body: str
    photos: list[SavedFile]

    @classmethod
    def from_post(cls, post: dict[str, Any], media: SavedMedia) -> Self:
        return cls(
            str(post["number"]), post["date"], post["text"].rstrip("\n"),
            media.photos(),
        )

    @property
    def year(self) -> str:
        return self.date[:4] if self.date else "xxx"

    @property
    def file(self) -> str:
        return f"{self.year}.md"

    @property
    def text(self) -> str:
        parts = ["---", f"# {self.number}"]
        if self.date:
            parts.append(f"_{self.date}_")
        if self.body:
            parts.append(self.body)
        parts.extend(file.markdown_image() for file in self.photos)
        return "\n\n".join(parts)

    def write(self, directory: Path) -> None:
        YearlyMarkdown(directory).save(self.number, self.year, self.text, self.file)


@dataclass
class MitovebuliSaver(PostSaver):
    number: str
    name: str
    date: str | None
    body: str
    rating: float | None
    location: dict[str, Any]
    uniqueness: int | None
    monumentality: int | None
    atmosphere: int | None
    liveliness: int | None
    photos: list[SavedFile]

    @classmethod
    def from_post(cls, post: dict[str, Any], media: SavedMedia) -> Self:
        extra = post["extra"] or {}
        return cls(
            number=str(post["number"]),
            name=post["name"],
            date=post["date"],
            body=post["text"].rstrip("\n"),
            rating=extra.get("rating"),
            location=extra.get("location") or {},
            uniqueness=extra.get("uniqueness"),
            monumentality=extra.get("monumentality"),
            atmosphere=extra.get("atmosphere"),
            liveliness=extra.get("liveliness"),
            photos=media.photos(),
        )

    @property
    def year(self) -> str:
        return self.date[:4] if self.date else "xxx"

    @property
    def file(self) -> str:
        return f"{self.year}.md"

    @property
    def text(self) -> str:
        parts = ["---", f"_{self.number}_ # {self.name}"]
        if self.rating is not None:
            parts.append(f"**{self.rating}**")
        if self.date:
            parts.append(f"_{self.date}_")
        if self.body:
            parts.append(self.body)
        link = self.location.get("link")
        if link:
            label = (
                f"{self.location['latitude']}, {self.location['longitude']}"
                if self.location.get("latitude") is not None
                and self.location.get("longitude") is not None else "Карта"
            )
            url = link if urlsplit(link).scheme else f"https://{link}"
            if urlsplit(url).scheme in {"http", "https"}:
                parts.append(f"[{label}]({url})")
        for label, value in (
            ("Уникальность", self.uniqueness),
            ("Монументальность", self.monumentality),
            ("Атмосфера", self.atmosphere),
            ("Жизненность", self.liveliness),
        ):
            parts.append(f"{label}: {value if value is not None else '—'}")
        parts.extend(file.markdown_image() for file in self.photos)
        return "\n\n".join(parts)

    def write(self, directory: Path) -> None:
        YearlyMarkdown(directory).save(self.number, self.year, self.text, self.file)


@dataclass
class PublikaSaver(PostSaver):
    number: str
    name: str
    date: str | None
    body: str

    @classmethod
    def extra_post_numbers(cls, post: dict[str, Any]) -> list[int]:
        return [-int(post["number"])] if INLINE_IMAGE.search(post["text"]) else []

    @classmethod
    def from_post(cls, post: dict[str, Any], media: SavedMedia) -> Self:
        return cls(
            str(post["number"]),
            post["name"],
            post["date"],
            localize_markdown_images(post["text"].rstrip("\n"), media),
        )

    @property
    def file(self) -> str:
        return f"{self.number}.md"

    @property
    def text(self) -> str:
        parts = [f"# {self.name}"]
        if self.date:
            parts.append(f"_{self.date}_")
        if self.body:
            parts.append(self.body)
        return "\n\n".join(parts)

    def write(self, directory: Path) -> None:
        (directory / self.file).write_text(self.text + "\n", encoding="utf-8")


@dataclass
class ShenishvnebiSaver(PostSaver):
    number: str
    name: str
    date: str | None
    body: str
    is_markdown: bool
    main: SavedFile | None
    attachments: list[SavedFile]

    @classmethod
    def extra_post_numbers(cls, post: dict[str, Any]) -> list[int]:
        if (post.get("extra") or {}).get("md") is True and INLINE_IMAGE.search(post["text"]):
            return [-int(post["number"])]
        return []

    @classmethod
    def from_post(cls, post: dict[str, Any], media: SavedMedia) -> Self:
        is_markdown = (post.get("extra") or {}).get("md") is True
        body = post["text"].rstrip("\n")
        if is_markdown:
            body = localize_markdown_images(body, media)
        return cls(
            str(post["number"]), post["name"], post["date"], body,
            is_markdown, media.main, media.attached_files(),
        )

    @property
    def year(self) -> str:
        return self.date[:4] if self.date else "xxx"

    @property
    def file(self) -> str:
        return f"{self.year}.md"

    @property
    def text(self) -> str:
        parts = ["---", f"# {self.number}"]
        if self.name:
            parts.append(f"## {self.name}")
        if self.date:
            parts.append(f"_{self.date}_")
        if self.body:
            parts.append(self.body)
        linked = linked_image_names(self.body) if self.is_markdown else set()
        for file in ([self.main] if self.main else []) + self.attachments:
            if file.name in linked:
                continue
            if file.media_type == "photo":
                parts.append(file.markdown_image())
            else:
                parts.append(f"[{file.name}](images/{quote(file.name, safe='')})")
        return "\n\n".join(parts)

    def write(self, directory: Path) -> None:
        YearlyMarkdown(directory).save(self.number, self.year, self.text, self.file)


@dataclass
class ChasatseriSaver(PostSaver):
    number: str
    name: str
    date: str | None
    body: str
    is_markdown: bool
    main: SavedFile | None
    attachments: list[SavedFile]

    @classmethod
    def extra_post_numbers(cls, post: dict[str, Any]) -> list[int]:
        if (post.get("extra") or {}).get("md") is True and INLINE_IMAGE.search(post["text"]):
            return [-int(post["number"])]
        return []

    @classmethod
    def from_post(cls, post: dict[str, Any], media: SavedMedia) -> Self:
        is_markdown = (post.get("extra") or {}).get("md") is True
        body = post["text"].rstrip("\n")
        if is_markdown:
            body = localize_markdown_images(body, media)
        return cls(
            str(post["number"]), post["name"], post["date"], body,
            is_markdown, media.main, media.attached_files(),
        )

    @property
    def year(self) -> str:
        return self.date[:4] if self.date else "xxx"

    @property
    def file(self) -> str:
        return f"{self.year}.md"

    @property
    def text(self) -> str:
        parts = ["---", f"# {self.number}"]
        if self.name:
            parts.append(f"## {self.name}")
        if self.date:
            parts.append(f"_{self.date}_")
        if self.body:
            parts.append(self.body)
        linked = linked_image_names(self.body) if self.is_markdown else set()
        for file in ([self.main] if self.main else []) + self.attachments:
            if file.name in linked:
                continue
            if file.media_type == "photo":
                parts.append(file.markdown_image())
            else:
                parts.append(f"[{file.name}](images/{quote(file.name, safe='')})")
        return "\n\n".join(parts)

    def write(self, directory: Path) -> None:
        YearlyMarkdown(directory).save(self.number, self.year, self.text, self.file)


@dataclass
class AnimeebiSaver(PostSaver):
    number: str
    name: str
    original_title: str
    year: int | None
    rating: int | None
    body: str
    result: str
    screenshots: list[SavedFile]

    @classmethod
    def from_post(cls, post: dict[str, Any], media: SavedMedia) -> Self:
        extra = post["extra"] or {}
        screenshots = [
            file for file in media.attached_files() if file.media_type == "photo"
        ][:3]
        return cls(
            number=str(post["number"]),
            name=post["name"],
            original_title=extra.get("original_title") or "",
            year=extra.get("year"),
            rating=extra.get("rating"),
            body=post["text"].rstrip("\n"),
            result=extra.get("result") or "",
            screenshots=screenshots,
        )

    @property
    def bucket(self) -> str:
        return str(int(self.number) // 1000)

    @property
    def file(self) -> str:
        return f"{self.bucket}.md"

    @property
    def text(self) -> str:
        parts = ["---", f"_{self.number}_", f"# {self.name}"]
        original_and_year = []
        if self.original_title:
            original_and_year.append(f"_{self.original_title}_")
        if self.year is not None:
            original_and_year.append(f"_{self.year}_")
        if original_and_year:
            parts.append(" · ".join(original_and_year))
        if self.rating is not None:
            parts.append(f"**{self.rating}**")
        if self.body:
            parts.append(self.body)
        if self.result:
            parts.append(f"стоит смотреть: {self.result}")
        parts.extend(file.markdown_image() for file in self.screenshots)
        return "\n\n".join(parts)

    def write(self, directory: Path) -> None:
        entries_path = directory / "info" / "animeebi_entries.json"
        entries = (
            json.loads(entries_path.read_text(encoding="utf-8"))
            if entries_path.exists() else {}
        )
        old_bucket = entries.get(self.number, {}).get("bucket")
        entries[self.number] = {"bucket": self.bucket, "content": self.text}
        entries_path.write_text(
            json.dumps(entries, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        for bucket in {self.bucket, old_bucket} - {None}:
            sections = [
                entries[number]["content"] for number in sorted(entries, key=int)
                if entries[number]["bucket"] == bucket
            ]
            target = directory / f"{bucket}.md"
            if sections:
                target.write_text("\n\n".join(sections) + "\n", encoding="utf-8")
            else:
                target.unlink(missing_ok=True)


SAVERS = {
    "leksebi": LeksebiSaver,
    "gancdebi": GancdebiSaver,
    "ikhvomedia": IkhvomediaSaver,
    "nacherchebi": NacherchebiSaver,
    "natserebi": NatserebiSaver,
    "nomrebi": NomrebiSaver,
    "nakhalebi": NakhalebiSaver,
    "sakhlugeba": SakhlugebaSaver,
    "karebi": KarebiSaver,
    "nadzerpi": NadzerpiSaver,
    "mokhetiale": MokhetialeSaver,
    "mitovebuli": MitovebuliSaver,
    "publika": PublikaSaver,
    "shenishvnebi": ShenishvnebiSaver,
    "chasatseri": ChasatseriSaver,
    "animeebi": AnimeebiSaver,
}


class SiteDownloader:
    def __init__(self, site_url: str, target: Path) -> None:
        self.site_url = site_url.rstrip("/")
        self.target = target
        self.session = requests.Session()

    def _get_json(
        self, path: str, data: dict[str, str] | None = None, csrf_token: str = ""
    ) -> dict[str, Any]:
        headers = {"Accept": "application/json"}
        if data is not None:
            headers.update({
                "X-CSRFToken": csrf_token,
                "Origin": self.site_url,
            })
            response = self.session.post(
                self.site_url + path, json=data, headers=headers, timeout=30
            )
        else:
            response = self.session.get(
                self.site_url + path, headers=headers, timeout=30
            )
        response.raise_for_status()
        return response.json()

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
        with self.session.get(url, stream=True, timeout=30) as response:
            response.raise_for_status()
            response.raw.decode_content = True
            with Image.open(response.raw) as source:
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
            with self.session.get(url, stream=True, timeout=30) as response:
                response.raise_for_status()
                response.raw.decode_content = True
                with temporary.open("wb") as output:
                    shutil.copyfileobj(response.raw, output)
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
        replace_existing: bool,
        extra_files: list[dict[str, Any]],
    ) -> SavedMedia:
        main_file = post["mainFile"]
        main = None
        seen_ids: set[str] = set()
        if main_file:
            name = self._download_file(main_file, directory, replace_existing)
            main = SavedFile(
                name,
                main_file["mediaType"],
                tuple(url for url in (main_file.get("linkFull"), main_file.get("link")) if url),
            )
            seen_ids.add(str(main_file["id"]))
        files = []
        public_files = []
        public_ids = {str(file["id"]) for file in post["files"]}
        for file in [*post["files"], *extra_files]:
            file_id = str(file["id"])
            if file_id in seen_ids:
                continue
            seen_ids.add(file_id)
            name = self._download_file(file, directory, replace_existing)
            saved = SavedFile(
                name,
                file["mediaType"],
                tuple(url for url in (file.get("linkFull"), file.get("link")) if url),
            )
            files.append(saved)
            if file_id in public_ids:
                public_files.append(saved)
        return SavedMedia(main, files, self.site_url, public_files)

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
        if not is_saved or post_number not in related:
            self._save_related_posts(post, info / "related.json", related)
        if not is_saved or post_number not in photos:
            saver_type = SAVERS.get(slug, RawJsonSaver)
            extra_files: list[dict[str, Any]] = []
            for draft_number in saver_type.extra_post_numbers(post):
                draft = self._get_json(f"/_api/formats/{slug}/{draft_number}/")
                if not draft.get("isDraft") or draft["number"] != draft_number:
                    raise ValueError(f"Ожидался черновик #{draft_number} формата {slug}")
                if draft["mainFile"]:
                    extra_files.append(draft["mainFile"])
                extra_files.extend(draft["files"])
            media = self._save_files(
                post, directory, replace_existing=not is_saved,
                extra_files=extra_files,
            )
            saver = saver_type.from_post(post, media)
            saver.write(directory)
            photos[post_number] = {
                "main": media.main.name if media.main else None,
                "files": [file.name for file in media.files],
            }
            (info / "photos.json").write_text(
                json.dumps(photos, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
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
        (info / "description.md").write_text(
            project["description"], encoding="utf-8"
        )
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


if __name__ == "__main__":
    SiteDownloader(SITE_URL, TARGET).run(USERNAME, PASSWORD, PROJECTS)
