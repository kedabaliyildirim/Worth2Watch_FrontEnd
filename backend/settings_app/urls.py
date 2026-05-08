from django.urls import path

from .views import (
    UpdateEmailView,
    UpdatePasswordView,
    UpdateProfilePictureView,
)

urlpatterns = [
    path("profile-picture", UpdateProfilePictureView.as_view()),
    path("email", UpdateEmailView.as_view()),
    path("password", UpdatePasswordView.as_view()),
]
