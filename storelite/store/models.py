from django.db import models
from django.contrib.auth.models import User

import os
from django.db.models.signals import post_delete
from django.dispatch import receiver

from uuid import uuid4
from django.utils.deconstruct import deconstructible

@deconstructible
class PathRename:
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = f'{uuid4().hex}.{ext}'
        return os.path.join(self.path, filename)
    
class Store(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=True)  
    store = models.CharField(max_length=100, unique=True)
    cnpj = models.CharField(max_length=18, unique=True, null=True)  

    layout = models.CharField(max_length=50, default='standard')  
    logo = models.ImageField(upload_to=PathRename('img/store/logo/'), blank=True, null=True)
    page = models.ImageField(upload_to=PathRename('img/store/page/'), blank=True, null=True)
    main = models.TextField(blank=True)
    draft = models.ImageField(upload_to=PathRename('img/store/draft/'), blank=True, null=True)
    text = models.TextField(blank=True)
    
    telephone = models.CharField(max_length=20, blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.store

@receiver(post_delete, sender=Store)
def delete_store_images(sender, instance, **kwargs):
    image_fields = ['logo', 'page', 'draft',]
    
    for field_name in image_fields:
        image = getattr(instance, field_name)
        if image and os.path.isfile(image.path):
            os.remove(image.path)