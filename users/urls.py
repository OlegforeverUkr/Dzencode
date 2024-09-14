from django.urls import path
from . import views

app_name = 'users'


urlpatterns = [
    path('registration/', view=views.UserRegistrationView.as_view(), name='registration'),
    path('login/', view=views.UserLoginView.as_view(), name='login'),
    path('logout/', view=views.UserLogoutView.as_view(), name='logout'),
    path('profile/', view=views.UserProfileView.as_view(), name='profile'),
]