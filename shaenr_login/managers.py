from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    """Manager for auth user accounts"""

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("User must have an email.")

        if not self.is_adult():
            raise ValueError("User must be an adult.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        if not user.is_adult():
            raise ValueError("")

        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)
