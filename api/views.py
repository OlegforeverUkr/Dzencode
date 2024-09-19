from rest_framework.permissions import IsAdminUser
from posts.models import Post, Comment

from api.serializers import PostSerializer, CommentSerializer
from rest_framework import generics
from rest_framework.response import Response


class PostApiView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentApiView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
