"""User self-service settings — port of v1 controllers/user.js.

All require a valid JWT (the user updates *their own* profile/email/
password); v1 also gated this with `isAuthenticated`. We mirror that
via DRF's `IsAuthenticated`."""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import UserSerializer


class UpdateProfilePictureView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        url = request.data.get("profile_picture") or request.data.get("profilePicture")
        if not isinstance(url, str):
            return Response(
                {"message": "profile_picture must be a string URL"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.user.profile_picture = url
        request.user.save(update_fields=["profile_picture"])
        return Response({"user": UserSerializer(request.user).data})


class UpdateEmailView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        email = request.data.get("email")
        if not email:
            return Response(
                {"message": "email is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.user.email = email
        request.user.save(update_fields=["email"])
        return Response({"user": UserSerializer(request.user).data})


class UpdatePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        password = request.data.get("password")
        if not password or len(password) < 6:
            return Response(
                {"message": "password must be at least 6 characters"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.user.set_password(password)
        request.user.save(update_fields=["password"])
        return Response({"user": UserSerializer(request.user).data})
