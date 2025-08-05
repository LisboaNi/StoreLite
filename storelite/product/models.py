from django.db import models
from django.contrib.auth.models import User
from store.models import Store

from uuid import uuid4
import os

def user_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join('product_images', filename)

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name = "Usuário")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="products", verbose_name = "Nome da Loja")
    name = models.CharField(max_length=100, unique=True, verbose_name = "Nome do Produto")
    description = models.TextField(verbose_name = "Descrição")
    photo = models.ImageField(upload_to=user_directory_path, verbose_name = "Foto")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name = "Valor")
    stock = models.PositiveIntegerField(verbose_name = "Quantidade no Estoque")
    number = models.CharField(max_length=20, blank=True, null=True, verbose_name = "Número")
    size = models.CharField(max_length=20, blank=True, null=True, verbose_name = "Tamanho")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = "Usuário")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name = "Nome da Loja")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name = "Produto")
    quantity = models.PositiveIntegerField(default=1, verbose_name = "Quantidade")

    class Meta:
        unique_together = ("user", "product", "store")

    class Meta:
        verbose_name = "Carrinho"
        verbose_name_plural = "Carrinho"

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) - {self.user.username}"
