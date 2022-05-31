from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from core.utility.managers import CustomUserManager


ROLES = {  # Roles that can be assigned to user
    ("customer", "Customer"),
    ("company", "Company"),
}


class UserRole(models.Model):  # User role (Customer or company)
    role = models.CharField(verbose_name="User`s role", max_length=15, choices=ROLES, null=False)

    def __str__(self):
        return self.role


class User(AbstractBaseUser, PermissionsMixin):  # Base user`s model overriding
    username = models.CharField(verbose_name="Username", max_length=30, unique=True)
    name = models.CharField(verbose_name="User`s name", max_length=150, null=False, default="default")
    email = models.EmailField(verbose_name="User`s email", null=False, unique=True)
    phone = models.CharField(verbose_name="User`s phone", max_length=100, null=False, default="0")
    role = models.ForeignKey(to=UserRole, on_delete=models.CASCADE, null=False)

    # User`s rights
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()  # Custom object manager for base user overloading

    USERNAME_FIELD = 'email'  # This field is user to log in with
    REQUIRED_FIELDS = ['username', 'name', 'phone', 'password', 'role']

    def __str__(self):  # Returns comprehensible representation of object
        return self.username
