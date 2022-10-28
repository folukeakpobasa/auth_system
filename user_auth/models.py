from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
import jwt
from datetime import datetime, timedelta
from django.conf import settings


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def token(self):
        token = jwt.encode({"full_name": self.full_name(), "email": self.email,
                            "exp": datetime.utcnow() + timedelta(hours=1)}, settings.SECRET_KEY, algorithm="HS256")
        return token


class Role(models.Model):
    ROLE = [
        ("customer", "customer"),
        ("supplier", "supplier"),
        ("staff", "staff"),

    ]

    user_role = models.CharField(max_length=20, choices=ROLE)
    created = models.DateTimeField(auto_now_add=True)
    custom_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='roles')

    def __str__(self):
        return self.user_role


class UserGroup(models.Model):
    GROUP_CHOICE = [
        ("A", "group A"),
        ("B", "group B"),
        ("C", "group C"),

    ]
    user_group = models.CharField(
        max_length=20, choices=GROUP_CHOICE)
    created = models.DateTimeField(auto_now_add=True)
    custom_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='user_groups', null=True)

    def __str__(self):
        return self.user_group
