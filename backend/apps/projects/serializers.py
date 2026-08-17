from __future__ import annotations

from pathlib import Path

from rest_framework import serializers

from apps.core.models import File, FileType

from .models import Post, Project, Tag


class FileSerializer(serializers.ModelSerializer):
    link = serializers.CharField(read_only=True)
    linkFull = serializers.CharField(source="link_full", read_only=True)
    mediaType = serializers.CharField(source="file_type", read_only=True)
    name = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ("id", "name", "link", "linkFull", "mediaType")

    def get_name(self, obj: File) -> str:
        return obj.original_name or Path(obj.content.name).name


class FileListSerializer(serializers.ModelSerializer):
    link = serializers.CharField(source="link_small", read_only=True)
    mediaType = serializers.CharField(source="file_type", read_only=True)

    class Meta:
        model = File
        fields = ("link", "mediaType")

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("code", "name")


class ProjectListSerializer(serializers.ModelSerializer):
    cover = serializers.CharField(source="cover.link", read_only=True)
    postType = serializers.CharField(source="post_type", read_only=True)
    postListType = serializers.CharField(source="post_list_type", read_only=True)
    isPublic = serializers.BooleanField(source="is_public", read_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "description",
            "link",
            "cover",
            "postType",
            "postListType",
            "isPublic",
            "status",
        )


class RelatedPostSerializer(serializers.ModelSerializer):
    link = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = ("number", "link")


class PostSerializer(serializers.ModelSerializer):
    link = serializers.CharField(read_only=True)
    projectCode = serializers.CharField(source="project.link", read_only=True)
    projectName = serializers.CharField(source="project.name", read_only=True)
    postType = serializers.CharField(source="project.post_type", read_only=True)
    mainFile = FileSerializer(source="main_file", read_only=True)
    files = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    relatedPost = RelatedPostSerializer(
        source="related_post",
        read_only=True,
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "number",
            "link",
            "projectCode",
            "projectName",
            "postType",
            "date",
            "name",
            "text",
            "mainFile",
            "files",
            "tags",
            "extra",
            "relatedPost",
        )

    def get_files(self, obj: Post) -> list[dict[str, object]]:
        files = [post_file.file for post_file in obj.post_files.all()]
        return list(FileSerializer(files, many=True).data)


class PostListSerializer(serializers.ModelSerializer):
    link = serializers.CharField(read_only=True)
    mainFile = FileListSerializer(source="main_file", read_only=True)
    rating = serializers.JSONField(read_only=True, allow_null=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "number",
            "link",
            "name",
            "text",
            "mainFile",
            "rating",
            "date",
        )


def post_summary_files(obj: Post) -> list[File]:
    files = ([obj.main_file] if obj.main_file else []) + [
        post_file.file for post_file in obj.post_files.all()
    ]
    return list({file.id: file for file in files}.values())


class GeneralPostListSerializer(serializers.ModelSerializer):
    link = serializers.CharField(read_only=True)
    label = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "number", "link", "label", "thumbnail", "date")

    def get_label(self, obj: Post) -> str:
        if obj.name.strip():
            return obj.name.strip()

        excerpt = " ".join(obj.text.split())
        if excerpt:
            return excerpt if len(excerpt) <= 120 else f"{excerpt[:117].rstrip()}..."

        counts = {
            FileType.PHOTO: 0,
            FileType.VIDEO: 0,
            FileType.AUDIO: 0,
            FileType.OTHER: 0,
        }
        for file in post_summary_files(obj):
            counts[file.file_type] += 1

        parts = [
            f"{emoji} {counts[file_type]}"
            for file_type, emoji in (
                (FileType.PHOTO, "📷"),
                (FileType.VIDEO, "🎬"),
                (FileType.AUDIO, "🎵"),
                (FileType.OTHER, "📎"),
            )
            if counts[file_type]
        ]
        return " · ".join(parts) or "🌀"

    def get_thumbnail(self, obj: Post) -> str | None:
        return next(
            (
                file.link_small
                for file in post_summary_files(obj)
                if file.file_type == FileType.PHOTO
            ),
            None,
        )
