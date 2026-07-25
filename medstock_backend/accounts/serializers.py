from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role', 'phone_number')

    def create(self, validated_data):
        # IMPORTANT: never save a raw password. create_user() hashes it
        # properly (PBKDF2 by default) before storing in the database.
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Used for the 'who am I' endpoint — never includes password."""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'phone_number')