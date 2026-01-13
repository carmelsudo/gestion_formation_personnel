from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser) : 
    avatar = models.ImageField(upload_to='images', null=True, blank=True)
    groupe = models.TextField(max_length=200, null=True, blank=True)
    def __str__(self) : 
        return self.username
    def save(self,*args , **kwargs):
        if(self.password) :
            self.set_password(raw_password=self.password)
        return super().save(*args , **kwargs)
    
