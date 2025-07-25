from django.urls import path
from .views import StoreFrontView

app_name = 'public'

urlpatterns = [
    path('<slug:store_name>/', StoreFrontView.as_view(), name='store_front'),
]
