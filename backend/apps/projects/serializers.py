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
    postCount = serializers.IntegerField(source="post_count", read_only=True)
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
            "postCount",
            "postType",
            "postListType",
            "isPublic",
            "status",
        )


def post_summary_files(obj: Post) -> list[File]:
    files = ([obj.main_file] if obj.main_file else []) + [
        post_file.file for post_file in obj.post_files.all()
    ]
    return list({file.id: file for file in files}.values())


class RelatedPostSerializer(serializers.ModelSerializer):
    link = serializers.CharField(read_only=True)
    label = serializers.CharField(source="display_label", read_only=True)
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "number", "link", "label", "thumbnail", "date")

    def get_thumbnail(self, obj: Post) -> str | None:
        return next(
            (
                file.link_small
                for file in post_summary_files(obj)
                if file.file_type == FileType.PHOTO
            ),
            None,
        )


class AdjacentPostSerializer(serializers.ModelSerializer):
    link = serializers.CharField(read_only=True)
    label = serializers.CharField(source="display_label", read_only=True)

    class Meta:
        model = Post
        fields = ("number", "link", "label")


class PostSerializer(serializers.ModelSerializer):
    link = serializers.CharField(read_only=True)
    projectCode = serializers.CharField(source="project.link", read_only=True)
    projectName = serializers.CharField(source="project.name", read_only=True)
    postType = serializers.CharField(source="project.post_type", read_only=True)
    mainFile = FileSerializer(source="main_file", read_only=True)
    files = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    relatedPosts = RelatedPostSerializer(
        source="related_posts",
        many=True,
        read_only=True,
    )
    previousPost = AdjacentPostSerializer(
        source="previous_post_summary",
        read_only=True,
    )
    nextPost = AdjacentPostSerializer(
        source="next_post_summary",
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
            "relatedPosts",
            "previousPost",
            "nextPost",
        )

    def get_files(self, obj: Post) -> list[dict[str, object]]:
        files = [post_file.file for post_file in obj.post_files.all()]
        return list(FileSerializer(files, many=True).data)


class PostListSerializer(serializers.ModelSerializer):
    link = serializers.CharField(read_only=True)
    label = serializers.CharField(source="display_label", read_only=True)
    cardFile = serializers.SerializerMethodField()
    rating = serializers.JSONField(read_only=True, allow_null=True)

    def get_cardFile(self, obj: Post) -> dict[str, str] | None:
        if obj.card_file_link is None or obj.card_file_type is None:
            return None
        return {
            "link": obj.card_file_link,
            "mediaType": obj.card_file_type,
        }

    class Meta:
        model = Post
        fields = (
            "id",
            "number",
            "link",
            "label",
            "cardFile",
            "rating",
            "date",
        )
