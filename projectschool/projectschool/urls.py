from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authorization.urls')),
    path('room/', include('authorization.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login', include('authorization.urls'), name='login'),
    path('accounts/register', include('authorization.urls'), name='register'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('OpenAPI/', include('social_django.urls', namespace='social')),
    path(r'accounts/profile/', include('authorization.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
