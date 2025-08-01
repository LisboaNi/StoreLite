from django.db import models
from django.contrib.auth.models import User

import os
from django.db.models.signals import post_delete
from django.dispatch import receiver

from uuid import uuid4
from django.utils.deconstruct import deconstructible

from django.utils.text import slugify
from django.urls import reverse

from colorfield.fields import ColorField

@deconstructible
class PathRename:
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        filename = f"{uuid4().hex}.{ext}"
        return os.path.join(self.path, filename)


class Store(models.Model):
    COLOR_CHOICES = [
        ("#0B2545", "Azul Profundo"),
        ("#e91e63", "Rosa Claro"),
        ("#3f51b5", "Azul Médio"),
        ("#fdd835", "Amarelo Claro"),
        ("#ffb74d", "Laranja Suave"),
        ("#ef5350", "Vermelho Suave"),
        ("#ba68c8", "Roxo Claro"),
        ("#4db6ac", "Verde Água"),
        ("#c62828", "Vermelho Pizzaria"),
        ("#2E4D38", "Verde Musgo Escuro"),
        ("#3A0B52", "Roxo Beringela"),
        ("#2e2e2e", "Grafite Escuro"),
        ("#7B1E1E", "Vermelho Vinho"),
        ("#8B4513", "Marrom Queimado"),
        ("#665c1e", "Mostarda Escura"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=True)
    store = models.CharField(max_length=100, unique=True)
    cnpj = models.CharField(max_length=18, unique=True, null=True)

    layout = models.CharField(max_length=50, default="standard")
    logo = models.ImageField(upload_to=PathRename("logo/"), blank=True, null=True)
    page = models.ImageField(upload_to=PathRename("page/"), blank=True, null=True)
    main = models.TextField(blank=True)
    draft = models.ImageField(upload_to=PathRename("draft/"), blank=True, null=True)
    text = models.TextField(blank=True)

    telephone = models.CharField(max_length=20, blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    slug = models.SlugField(unique=True, blank=True)
    primary_color = ColorField(max_length=7, choices=COLOR_CHOICES, default="#0B2545")

    def __str__(self):
        return self.store

    def save(self, *args, **kwargs):
        new_slug = slugify(self.store)
        if self.slug != new_slug:
            self.slug = new_slug
        super().save(*args, **kwargs)

    def get_store_url(self):
        if self.slug:
            return reverse("public:store_front", args=[self.slug])
        return "#"


@receiver(post_delete, sender=Store)
def delete_store_images(sender, instance, **kwargs):
    image_fields = [
        "logo",
        "page",
        "draft",
    ]

    for field_name in image_fields:
        image = getattr(instance, field_name)
        if image and os.path.isfile(image.path):
            os.remove(image.path)


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.user.username
