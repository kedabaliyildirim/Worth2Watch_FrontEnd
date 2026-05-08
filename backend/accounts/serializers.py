from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id", "email", "name", "surname",
            "profile_picture", "role", "birth_date", "gender",
        )
        read_only_fields = ("id", "role")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = (
            "email", "password", "name", "surname",
            "profile_picture", "birth_date", "gender",
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


def tokens_for(user):
    """Return {access, refresh} tokens for a user.

    The v1 Express endpoint returned a single `token` field; we expose
    both DRF SimpleJWT tokens (access + refresh) so the frontend can
    silently refresh — backwards-compatible since `token` is just an
    alias for `access`."""
    refresh = RefreshToken.for_user(user)
    refresh["role"] = user.role  # mirrors v1's JWT payload shape
    return {
        "token": str(refresh.access_token),
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }
