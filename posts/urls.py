from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('<int:pk>/', views.PostView.as_view(), name='post_detail'),
]