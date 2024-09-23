from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from api.filters import ComfortableOrderingFilter
from api.permissions import IsOwnerOrAdmin
from api.post_pagination import PostPaginator

from posts.models import Post, Comment
from api.serializers import CustomCommentsSerializer, PostSerializer, CommentSerializer



class PostsViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, ComfortableOrderingFilter]
    ordering_fields = ["username", "email", "created", "updated"]
    ordering = ['-created_at']
    pagination_class = PostPaginator


    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated(), IsOwnerOrAdmin()]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def list(self, request, *args, **kwargs):
        cache_key = "posts_list"
        posts = cache.get(cache_key)

        if posts is None:
            response = super().list(request, *args, **kwargs)
            posts = response.data
            cache.set(cache_key, posts, 60 * 5)
            return response
        else:
            return Response(posts)


    @action(methods=["get"], detail=False, permission_classes=[AllowAny])
    def comments(self, request):
        cache_key = "comments_list"
        comments = cache.get(cache_key)

        if comments is None:
            comments = Comment.objects.all()
            serializer = CustomCommentsSerializer(comments, many=True)
            cache.set(cache_key, serializer.data, 60 * 5)
            return Response({"comments": serializer.data})
        else:
            return Response({"comments": comments})


class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


    def get_permissions(self):
        if self.action in ["list", "retrive"]:
            return [AllowAny()]
        return [IsAuthenticated(), IsOwnerOrAdmin()]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 
