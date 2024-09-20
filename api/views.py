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


    @action(methods=["get"], detail=False, permission_classes=[AllowAny])
    def comments(self, request):
        comments = Comment.objects.all()
        serializer = CustomCommentsSerializer(comments, many=True)
        return Response({"comments": serializer.data})


class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


    def get_permissions(self):
        if self.action in ["list", "retrive"]:
            return [AllowAny()]
        return [IsAuthenticated(), IsOwnerOrAdmin()]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 
