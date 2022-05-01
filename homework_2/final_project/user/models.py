from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager


class UserProfile(AbstractBaseUser, PermissionsMixin):  # Extends capabilities of basic Django user
    fullname = models.CharField(verbose_name="User`s fullname", max_length=256)
    username = models.CharField(verbose_name="User`s nickname", max_length=100, unique=True)
    age = models.IntegerField(verbose_name="User`s age")
    phone = models.CharField(verbose_name="User`s phone number", max_length=100)
    email = models.EmailField(verbose_name="User`s email", unique=True)
    city = models.CharField(verbose_name="User`s city", max_length=256)
    profile_image = models.ImageField(verbose_name="Profile image", upload_to="images/profile_images/")

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fullname", "username"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username}-({self.fullname})"
