from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
    tokens_for,
)


class RegisterView(APIView):
    """POST /auth/register — mirrors v1 controller exactly.

    v1 returned 400 for duplicate email and 400 for short password; same
    here, and the success response shape preserves `{status, user, token}`.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        if User.objects.filter(email__iexact=request.data.get("email", "")).exists():
            return Response(
                {"message": "User already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "status": "OK",
                "user": UserSerializer(user).data,
                **tokens_for(user),
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """POST /auth/login — email + password → JWT pair."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if not user.check_password(password):
            return Response(
                {"message": "Password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "status": "OK",
                "user": UserSerializer(user).data,
                **tokens_for(user),
            }
        )
