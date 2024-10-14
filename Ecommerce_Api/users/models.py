from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self,email,password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None, **extra_fields):
        user =self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, max_length=255)
    password = models.CharField(max_length=128, blank=False, null=False, unique=True )
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Profile(models.Model):
    first_name = models.CharField(max_length=50, unique = False )
    last_name = models.CharField(max_length=50, unique = False) 
    username = models.CharField(max_length=50, unique=True )
    picture = models.URLField(null=True, blank=True)
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
 

