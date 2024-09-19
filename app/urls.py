from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from app import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),

    path('api/', include('rest_framework.urls', namespace="rest_framework")),
    path('api/', include('api.urls', namespace='api')),
    path('', include('users.urls', namespace='user')),
    path('', include('posts.urls', namespace='post')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)