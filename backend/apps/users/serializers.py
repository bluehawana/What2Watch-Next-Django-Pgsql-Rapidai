"""
Serializers for users app.
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, ProfileType, UserProfile


class ProfileTypeSerializer(serializers.ModelSerializer):
    """Serializer for ProfileType model."""
    class Meta:
        model = ProfileType
        fields = ['id', 'name', 'display_name', 'description', 'icon']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model."""
    profile_types = ProfileTypeSerializer(many=True, read_only=True)
    profile_type_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=ProfileType.objects.all(),
        source='profile_types',
        write_only=True
    )
    subscribed_services = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'id', 'profile_types', 'profile_type_ids', 'timezone', 'language',
            'notifications_enabled', 'email_notifications', 'push_notifications',
            'has_netflix', 'has_prime_video', 'has_disney_plus', 'has_hbo_max',
            'has_hulu', 'has_apple_tv_plus', 'has_paramount_plus', 'has_peacock',
            'subscribed_services', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_subscribed_services(self, obj):
        """Get list of subscribed streaming services."""
        return obj.get_subscribed_services()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'profile_image', 'bio', 'date_of_birth', 'profile',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'email', 'username', 'password', 'password2',
            'first_name', 'last_name'
        ]

    def validate(self, attrs):
        """Validate password matching."""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        return attrs

    def create(self, validated_data):
        """Create user with hashed password and profile."""
        validated_data.pop('password2')
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        # Create associated profile
        UserProfile.objects.create(user=user)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user information."""
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'profile_image',
            'bio', 'date_of_birth'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change endpoint."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
