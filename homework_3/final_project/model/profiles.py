from django.db import models


ROLES = {  # Roles that can be assigned to user
    ("customer", "Customer"),
    ("company", "Company"),
}


class UserRole(models.Model):  # User role (Customer or company)
    role = models.CharField(verbose_name="User`s role", max_length=15, choices=ROLES, null=False)

    def __str__(self):
        return self.role


class User(models.Model):  # Base user`s model
    name = models.CharField(verbose_name="User`s name", max_length=150, null=False)
    email = models.EmailField(verbose_name="User`s email", null=False)
    phone = models.CharField(verbose_name="User`s phone", max_length=100, null=False)
    role = models.ForeignKey(to=UserRole, on_delete=models.CASCADE, null=False)

    def __str__(self):  # Returns comprehensible representation of object
        return self.name
