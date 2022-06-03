from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):  # Custom manager for overriding base user model
    def create_user(self, username, name, email, phone, role, password, **extra_fields):  # Creates common user
        if not email:
            raise ValueError("There should be email !")
        user = self.model(username=username, name=name, email=email, phone=phone, role=role, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, name, role, email, phone, password, **extra_fields):  # Creates superuser
        # Setting access settings
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser`s 'is_staff' must be True !")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser 'is_staff' must be True !")
        return self.create_user(username, name, email, phone, role, password, **extra_fields)