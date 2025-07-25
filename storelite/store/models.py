from django.db import models
from django.contrib.auth.models import User

class Store(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    store = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, blank=True, null=True)  
    layout = models.CharField(max_length=50, default='standard')  
    logo = models.ImageField(upload_to='logo/', blank=True, null=True)
    page = models.ImageField(upload_to='page/', blank=True, null=True)
    main = models.TextField(blank=True)
    draft = models.ImageField(upload_to='draft/', blank=True, null=True)
    text = models.TextField(blank=True)
    
    telephone = models.CharField(max_length=20, blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.store