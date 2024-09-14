from django.contrib import admin
from posts.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "created_at"]
    list_editable = ["title"]
    search_fields = ["user__username", "title"]
    list_filter = ["user", "created_at"]
    fields = ["user", "title", "body"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "created_at"]
    search_fields = ["user__username", "post__title"]
    list_filter = ["user", "post", "created_at"]
    fields = [("post", "user"), "body", "image", "file"]
