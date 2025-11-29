"""
Admin configuration for users app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, ProfileType, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin for custom User model."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name', 'profile_image', 'bio', 'date_of_birth')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-created_at',)


@admin.register(ProfileType)
class ProfileTypeAdmin(admin.ModelAdmin):
    """Admin for ProfileType model."""
    list_display = ('display_name', 'name', 'icon', 'created_at')
    search_fields = ('display_name', 'name', 'description')
    ordering = ('display_name',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin for UserProfile model."""
    list_display = ('user', 'timezone', 'language', 'notifications_enabled', 'get_services')
    list_filter = ('notifications_enabled', 'email_notifications', 'push_notifications')
    search_fields = ('user__email', 'user__username')
    filter_horizontal = ('profile_types',)

    def get_services(self, obj):
        """Display subscribed streaming services."""
        return ', '.join(obj.get_subscribed_services()) or 'None'
    get_services.short_description = 'Streaming Services'
