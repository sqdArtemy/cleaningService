from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.utility.managers import CustomUserManager

from .service import Service

ROLES = (  # Roles that can be assigned to user
    ("customer", "Customer"),
    ("company", "Company"),
)


class UserRole(models.Model):  # User role (Customer or company)
    role = models.CharField(verbose_name="User`s role", max_length=15, choices=ROLES, null=False)

    def __str__(self):
        return self.role


class User(AbstractBaseUser, PermissionsMixin):  # Base user`s model overriding
    profile_pic = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    username = models.CharField(verbose_name="Username", max_length=30, unique=True)
    name = models.CharField(verbose_name="User`s name", max_length=150, null=False, default="default")
    email = models.EmailField(verbose_name="User`s email", null=False, unique=True)
    country = models.CharField(verbose_name="Country", max_length=50, null=False)
    city = models.CharField(verbose_name="City", max_length=50, null=False)
    address_details = models.CharField(verbose_name="District, house, apartment", max_length=256, null=False)
    services = models.ManyToManyField(verbose_name="Company`s services", to=Service)
    phone = models.CharField(verbose_name="User`s phone", max_length=100, null=False, default="0")
    role = models.ForeignKey(to=UserRole, on_delete=models.CASCADE, null=False)
    hour_cost = models.FloatField(verbose_name="Cost per working hour", null=False, validators=(MinValueValidator(0),))
    rating = models.FloatField(verbose_name="Star-rating", default=0, null=False, validators=(
        MaxValueValidator(5), MinValueValidator(0)))
    users_rated = models.PositiveIntegerField(verbose_name="Number of user rated", default=0)

    # User`s rights
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()  # Custom object manager for base user overloading

    USERNAME_FIELD = 'email'  # This field is user to log in with
    REQUIRED_FIELDS = ['username', 'name', 'phone', 'password', 'role', 'country', 'city', 'address_details']

    def __str__(self):  # Returns comprehensible representation of object
        return self.username
