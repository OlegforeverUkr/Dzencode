from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('add-post/', views.CreatePostView.as_view(), name='add_post'),
    path('<int:pk>/', views.PostsView.as_view(), name='post_detail'),
    path('<int:post_id>/add_comment/', views.AddCommentToPostView.as_view(), name='add_post_comment'),
    path('<int:pk>/delete-post/', views.DeletePostView.as_view(), name='delete_post'),
    path('<int:post_id>/<int:comment_id>/', views.AddCommentToCommentView.as_view(), name='add_comment_comment'),
    path('<int:pk>/delete-comment', views.DeleteCommentView.as_view(), name='delete_comment'),
]