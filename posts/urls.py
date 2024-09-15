from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('<int:pk>/', views.PostView.as_view(), name='post_detail'),
    path('<int:post_id>/<int:comment_id>/', views.AddCommentView.as_view(), name='add_comment_comment'),
    path('<int:post_id>/add_comment/', views.AddCommentView.as_view(), name='add_post_comment'),
]