from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

from django.conf import settings


class UsuarioManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))

        user = self.model(email=self.normalize_email(email),
                          username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        if settings.EMAIL_USE:
            self.send_verify_email(user, 'email', True)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email, username, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
