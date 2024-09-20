from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from django.urls import path, include
from api import views
from api.token_view import AddUsernameTokenObtainPairView


app_name = "api"

router = routers.DefaultRouter()
router.register(prefix=r"posts", viewset=views.PostsViewset, basename="post")
router.register(prefix=r"comments", viewset=views.CommentViewset, basename="comment")


urlpatterns = [
    path('token/', AddUsernameTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include(router.urls)),
]
