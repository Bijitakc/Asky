from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    GENDER_CHOICES=(
        ('M','M'),
        ('F','F'),
        ('O','0')
    )
    gender=models.CharField(max_length=1)
    bio=models.TextField()

    REQUIRED_FIELDS=[]

    def __str__(self):
        return self.username

    class Meta:
        verbose_name="CustomUser"
        verbose_name_plural="CustomUsers"

        
    