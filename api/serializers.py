from rest_framework import serializers
from posts.models import Post, Comment
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "user", "title", "body", "url", "created_at", "updated_at")

    def get_created_at(self, obj):
        return obj.created_at.strftime("%H:%M:%S %d:%m:%Y")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%H:%M:%S %d:%m:%Y")



class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("id", "user", "post", "body", "image", "file", "url", "parent", "created_at", "updated_at")

    def get_created_at(self, obj):
        return obj.created_at.strftime("%H:%M:%S %d:%m:%Y")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%H:%M:%S %d:%m:%Y")