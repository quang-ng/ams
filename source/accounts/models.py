from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as AbstractUserManager


class Family(models.Model):
    name = models.TextField(max_length=200, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MyUser(AbstractUser):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


class Activation(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
