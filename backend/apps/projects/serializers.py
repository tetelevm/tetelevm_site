from __future__ import annotations

from pathlib import Path

from rest_framework import serializers

from apps.core.models import File

from .models import Post, Project, Tag

IMAGE_SUFFIXES = {".avif", ".gif", ".jpeg", ".jpg", ".png", ".webp"}
VIDEO_SUFFIXES = {".m4v", ".mov", ".mp4", ".ogg", ".ogv", ".webm"}


def file_media_type(obj: File) -> str:
    suffix = Path(obj.original_name or obj.content.name).suffix.lower()
    if obj.preview or suffix in IMAGE_SUFFIXES:
        return "image"
    if suffix in VIDEO_SUFFIXES:
        return "video"
    return "file"


class FileSerializer(serializers.ModelSerializer):
    link = serializers.CharField(read_only=True)
    linkFull = serializers.CharField(source="link_full", read_only=True)
    mediaType = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ("id", "link", "linkFull", "mediaType")

    def get_mediaType(self, obj: File) -> str:
        return file_media_type(obj)


class FileListSerializer(serializers.ModelSerializer):
    link = serializers.CharField(source="link_small", read_only=True)
    mediaType = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ("link", "mediaType")

    def get_mediaType(self, obj: File) -> str:
        return file_media_type(obj)


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


class PostSerializer(serializers.ModelSerializer):
    link = serializers.CharField(read_only=True)
    projectCode = serializers.CharField(source="project.link", read_only=True)
    projectName = serializers.CharField(source="project.name", read_only=True)
    postType = serializers.CharField(source="project.post_type", read_only=True)
    mainFile = FileSerializer(source="main_file", read_only=True)
    files = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    relatedPost = serializers.IntegerField(
        source="related_post.number",
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
    date = serializers.JSONField(read_only=True, allow_null=True)

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
