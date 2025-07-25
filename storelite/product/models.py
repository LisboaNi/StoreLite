from django.db import models
from django.contrib.auth.models import User
from store.models import Store

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
    
class Product(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)  
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products') 
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    photo = models.ImageField(upload_to=PathRename('img/product/photo/'))
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    number = models.CharField(max_length=20, blank=True, null=True)
    size = models.CharField(max_length=20, blank=True, null=True) 

    def __str__(self):
        return self.name
    
@receiver(post_delete, sender=Product)
def delete_product_images(sender, instance, **kwargs):
    image_fields = ['photo',]
    
    for field_name in image_fields:
        image = getattr(instance, field_name)
        if image and os.path.isfile(image.path):
            os.remove(image.path)