from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AdminManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est requis")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)

class Admin(AbstractBaseUser):
    POST_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('admin_artist', 'Admin Artist'),
        ('admin_user', 'Admin User'),
        ('admin_galery', 'Admin Galery'),
        ('admin_paiment', 'Admin Paiment'),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    cin = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)
    post = models.CharField(max_length=20, choices=POST_CHOICES)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = AdminManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'post']

    def __str__(self):
        return self.email
