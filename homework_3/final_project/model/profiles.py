from django.db import models


ROLES = {  # Roles that can be assigned to user
    ("customer", "Customer"),
    ("company", "Company"),
}


class UserRole(models.Model):  # User role (Customer or company)
    role = models.CharField(verbose_name="User`s role", max_length=15, choices=ROLES)

    def __str__(self):
        return self.role


class User(models.Model):  # Base user`s model
    name = models.CharField(verbose_name="User`s name", max_length=150)
    email = models.EmailField(verbose_name="User`s email")
    phone = models.CharField(verbose_name="User`s phone", max_length=100)
    role = models.ForeignKey(to=UserRole, on_delete=models.CASCADE)

    def __str__(self):  # Returns comprehensible representation of object
        return self.name
