from django import template
from django.db import models
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

register = template.Library()

# Create your models here.


@register.filter
def to_class_name(value):
    return value.__class__.__name__

class Home(models.Model):
    HOME_TYPES = (
        ('landed', 'Landed'),
        ('condominium', 'Condominium'),
    )
    home_name = models.CharField(max_length=200, unique=True)
    home_address = models.CharField(max_length=300)
    house_type = models.CharField(max_length=50, choices=HOME_TYPES)
    def __str__(self):
        return self.home_name
      
class Human(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    human_name = models.CharField(max_length=200, unique=True)
    human_gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    human_date_of_birth = models.DateField('date of birth')
    human_description = models.CharField(max_length=300)
    human_home = models.ForeignKey(Home,related_name='home',on_delete=models.CASCADE)
    def __str__(self):
        return self.human_name
    
class Breed(models.Model):
    breed_name = models.CharField(max_length=100, unique=True)
    breed_origin = models.CharField(max_length=100)
    breed_description = models.CharField(max_length=300)
    def __str__(self):
        return self.breed_name
    
class Cat(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    cat_name = models.CharField(max_length=200, unique=True)
    cat_gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    cat_date_of_birth = models.DateField('date of birth')
    cat_description = models.CharField(max_length=300)
    cat_breed = models.ForeignKey(Breed,related_name='cats',on_delete=models.CASCADE)
    cat_owner = models.ForeignKey(Human,related_name='owned_cats',on_delete=models.CASCADE)

    def __str__(self):
        return self.cat_name
    

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

