from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for reading/updating the authenticated user profile."""

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'phone']
        read_only_fields = ['id', 'email']
        extra_kwargs = {
            'email': {'help_text': 'Unique email address (read-only after registration).'},
            'username': {'help_text': 'Display name visible to other users.'},
            'phone': {'help_text': 'Contact phone number in international format, e.g. +77001234567.'},
        }


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for creating a new user account."""

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text='Account password (min 8 characters). Write-only — never returned in responses.',
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'phone', 'password']
        extra_kwargs = {
            'email': {'help_text': 'Unique email address used for login.'},
            'username': {'help_text': 'Display name.'},
            'phone': {'help_text': 'Unique phone number, e.g. +77001234567.'},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            phone=validated_data['phone'],
            password=validated_data['password'],
        )
        return user
