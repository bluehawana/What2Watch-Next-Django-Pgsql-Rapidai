"""
URL configuration for what2watch project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.admin_view),

    # API Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API endpoints
    path('api/users/', include('apps.users.urls')),
    path('api/content/', include('apps.content.urls')),
    path('api/preferences/', include('apps.preferences.urls')),
    path('api/recommendations/', include('apps.recommendations.urls')),
]

# Debug toolbar (only in development)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API root documentation
admin.site.site_header = "What2Watch Admin"
admin.site.site_title = "What2Watch Admin Portal"
admin.site.index_title = "Welcome to What2Watch Administration"
