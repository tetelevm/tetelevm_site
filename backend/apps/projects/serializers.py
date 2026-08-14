from __future__ import annotations

from rest_framework import serializers

from .models import Post, Project


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
            "link",
            "cover",
            "postType",
            "postListType",
            "isPublic",
            "status",
        )


class PostSerializer(serializers.ModelSerializer):
    link = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "number", "link", "name", "text", "extra")


class ProjectDetailSerializer(ProjectListSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta(ProjectListSerializer.Meta):
        fields = (*ProjectListSerializer.Meta.fields, "posts")
