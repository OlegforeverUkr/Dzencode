from rest_framework import routers
from django.urls import path, include
from api import views


app_name = 'api'

router = routers.DefaultRouter()
router.register(prefix=r"posts", viewset=views.PostsViewset, basename="post")
router.register(prefix=r"comments", viewset=views.CommentViewset, basename="comment")


urlpatterns = [
    path('', include(router.urls)),
]
