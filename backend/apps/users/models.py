"""
User models for What2Watch application.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    """
    email = models.EmailField(_('email address'), unique=True)
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True, max_length=500)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Email as the primary identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']

    def __str__(self):
        return self.email


class ProfileType(models.Model):
    """
    Profile types for personalized recommendations.
    Examples: Hacker, Sports fan, Home lady, Home daddy, Kids, Family
    """
    PROFILE_CHOICES = [
        ('HACKER', 'Hacker'),
        ('SPORTS_FAN', 'Sports Fan'),
        ('HOME_LADY', 'Home Lady'),
        ('HOME_DADDY', 'Home Daddy'),
        ('KIDS', 'Kids'),
        ('FAMILY', 'Family'),
        ('MOVIE_BUFF', 'Movie Buff'),
        ('TV_SERIES', 'TV Series Enthusiast'),
        ('DOCUMENTARY', 'Documentary Lover'),
        ('CUSTOM', 'Custom'),
    ]

    name = models.CharField(max_length=50, choices=PROFILE_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)  # For emoji or icon class
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('profile type')
        verbose_name_plural = _('profile types')
        ordering = ['display_name']

    def __str__(self):
        return self.display_name


class UserProfile(models.Model):
    """
    User profile with preferences and selected profile types.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    profile_types = models.ManyToManyField(
        ProfileType,
        related_name='users',
        blank=True
    )
    timezone = models.CharField(max_length=50, default='UTC')
    language = models.CharField(max_length=10, default='en')
    notifications_enabled = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)

    # Streaming service subscriptions
    has_netflix = models.BooleanField(default=False)
    has_prime_video = models.BooleanField(default=False)
    has_disney_plus = models.BooleanField(default=False)
    has_hbo_max = models.BooleanField(default=False)
    has_hulu = models.BooleanField(default=False)
    has_apple_tv_plus = models.BooleanField(default=False)
    has_paramount_plus = models.BooleanField(default=False)
    has_peacock = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

    def __str__(self):
        return f"{self.user.email}'s profile"

    def get_subscribed_services(self):
        """Returns list of streaming services user is subscribed to."""
        services = []
        if self.has_netflix:
            services.append('Netflix')
        if self.has_prime_video:
            services.append('Prime Video')
        if self.has_disney_plus:
            services.append('Disney+')
        if self.has_hbo_max:
            services.append('HBO Max')
        if self.has_hulu:
            services.append('Hulu')
        if self.has_apple_tv_plus:
            services.append('Apple TV+')
        if self.has_paramount_plus:
            services.append('Paramount+')
        if self.has_peacock:
            services.append('Peacock')
        return services
