from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.


class CustomUser(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_active") is not True:
            raise ValueError(
                "Admin must have the is_active attribute set to true")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Admin must have is_active attribute set to True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Admin must have is_active attribute set to True")

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):
    email = models.CharField(max_length=250, unique=True, null=False, blank=False)
    REGISTRATION_CHOICES = [
        ('email', 'Email'),
        ('google', 'Google'),
    ]
    registration_method = models.CharField(
        max_length=10,
        choices=REGISTRATION_CHOICES,
        default='email'
    )

    objects = CustomUser()

    USERNAME_FIELD = "email"
    
    REQUIRED_FIELDS = []

    def __str__(self):
       return self.username
