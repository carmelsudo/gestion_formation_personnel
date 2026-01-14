from django.db import models
from django.contrib.auth.models import AbstractUser
from Service.models import *
# Create your models here.
class goupeChoices(models.TextChoices):
        ADMIN = 'admin', 'ADMIN'
        CHEF = 'chef', 'CHEF'
        EMPLOYE = 'employe', 'EMPLOYE'
class User(AbstractUser) : 
    avatar = models.ImageField(upload_to='images', null=True, blank=True)
    groupe = models.CharField(
            max_length=10,
            choices=goupeChoices.choices,
            default=goupeChoices.EMPLOYE
        )
    def __str__(self) : 
        return self.username
    def save(self, *args, **kwargs):
        if not self.pk :
            self.set_password(self.password)
        
        return  super().save(*args, **kwargs)
    @property
    def subordonnee(self) : 
        service = ServiceGerant.objects.filter(user = self ).first().service
        services = service.get_all_subservices  
        servicegerants  = ServiceGerant.objects.filter( service__in= services )
        return servicegerants.exclude(user = self)
