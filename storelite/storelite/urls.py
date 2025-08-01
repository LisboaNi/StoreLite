from django.urls import path
from . import views

app_name = "storelite"

urlpatterns = [
    path('', views.home, name='home'), 
]
