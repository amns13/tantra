from rest_framework import serializers

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializes registration requests and creates a new user"""
    password = serializers.CharField(
        max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'full_name',
            'password'
        )

    def create(self, validated_data) -> User:
        return User.objects.create_user(**validated_data)
