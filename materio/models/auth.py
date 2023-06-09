from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.db import models


class CustomerUserManager(UserManager):
    def create_user(self, phone, password=None, is_staff=False, is_superuser=False, is_active=True, **extra_fields):
        user = self.model(phone=phone, password=password, is_staff=is_staff, is_superuser=is_superuser,
                          is_active=is_active)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        return self.create_user(phone=phone, password=password, is_staff=True, is_superuser=True, is_active=True,
                                **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=128, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, unique=True)
    last_name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=128)

    user_type = models.SmallIntegerField(default=0)

    is_superuser = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    objects = CustomerUserManager()

    USERNAME_FIELD = 'username'


class OTP(models.Model):
    phone = models.CharField(max_length=20)
    key = models.CharField(max_length=512)

    is_conf = models.BooleanField(default=False)
    is_expire = models.BooleanField(default=False)
    tries = models.SmallIntegerField(default=0)

    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.tries >= 3:
            self.is_expire = True

        super(OTP, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.phone}'
