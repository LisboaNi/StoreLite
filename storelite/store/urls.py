from django.urls import path
from .views import StoreView

urlpatterns = [
    path("register/", StoreView.as_view(), name="register"),
]
