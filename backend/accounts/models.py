"""Custom User mirroring the v1 Mongoose schema field-for-field.

v1 (begumis/Movie_App, models/user.js) shape:
  name, surname, email, password, profilePicture, role (admin|user),
  birthDate, gender

Django's AbstractUser already covers email + password + a username slot;
we drop the username requirement (login is by email) and add the rest.
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Email-as-username manager."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("role", "user")
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("user", "User"),
    )

    # Drop username, use email as the login identifier.
    username = None
    email = models.EmailField(unique=True)

    # v1 schema fields.
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120)
    profile_picture = models.URLField(max_length=500, blank=True, default="")
    role = models.CharField(max_length=8, choices=ROLE_CHOICES, default="user")
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True, default="")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"
