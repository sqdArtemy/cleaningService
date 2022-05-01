from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user manager that is used to configure login ang registering setting of a user
    """

    def create_user(self, nickname, fullname, email, password, **extra_fields):
        """
        Creates and saves user with specified data
        """

        if not email:
            raise ValueError("E-mail should be entered!")
        user = self.model(nickname=nickname, fullname=fullname, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, nickname, fullname, email, password, **extra_fields):
        """
        Creates and saves superuser with custom parameters
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError('Variable "is_staff" should be true!')
        if extra_fields.get("is_superuser") is not True:
            raise ValueError('Variable "is_superuser" should be true!')
        return self.create_user(nickname, fullname, email, password, **extra_fields)
