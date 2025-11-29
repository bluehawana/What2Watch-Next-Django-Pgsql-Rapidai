"""
URL configuration for users app.
"""
from django.urls import path
from .views import (
    UserRegistrationView,
    UserProfileView,
    UserUpdateView,
    ChangePasswordView,
    ProfileTypeListView,
    UserProfileDetailView,
    current_user,
)

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('me/', current_user, name='current_user'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/update/', UserUpdateView.as_view(), name='user_update'),
    path('profile/preferences/', UserProfileDetailView.as_view(), name='user_preferences'),
    path('password/change/', ChangePasswordView.as_view(), name='change_password'),
    path('profile-types/', ProfileTypeListView.as_view(), name='profile_types'),
]
