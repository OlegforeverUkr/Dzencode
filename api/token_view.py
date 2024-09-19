from rest_framework_simplejwt.views import TokenObtainPairView

from api.token_serializer import AddUsernameTokenSerializer


class AddUsernameTokenObtainPairView(TokenObtainPairView):
    serializer_class = AddUsernameTokenSerializer