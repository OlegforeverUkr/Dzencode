from rest_framework import routers
from django.urls import path, include
from api import views


app_name = 'api'

urlpatterns = [
    path('posts/', views.PostApiView.as_view(), name="posts"),
    path('comments/', views.CommentApiView.as_view(), name="comments"),
]
