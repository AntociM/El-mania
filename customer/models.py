from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin

from django_countries.fields import CountryField

# Create your models here.

class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user = self._create_user(
            username, email, password, True, True, **extra_fields)
        return user


class UserProfile(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)


class UserContact(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, null=True, blank=True)
    email = models.EmailField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=80, null=True, blank=True)
    city = models.CharField(max_length=40, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    country = CountryField(null=True, blank=True)

class Contact(models.Model):
    REPLIED = ((0, 'No'), (1, 'Yes'))
    name = models.CharField(max_length=100, null=False, blank=False)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(
        max_length=50, blank=False)
    title = models.CharField(max_length=100, null=False, blank=False, default=None)
    message = models.TextField(blank=False, null=False)
    replied = models.IntegerField(choices=REPLIED, default=False)
    created = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)