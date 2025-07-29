from django.urls import path
from .views import (
    StoreFrontView,
    ProductListView,
    UserView,
    ClientLoginView,
    ClientProfileView,
    StoreLogoutView,
    AddToCartView,
    CartView,
    RemoveFromCartView,
)

app_name = "public"

urlpatterns = [
    path("<slug:store_name>/", StoreFrontView.as_view(), name="store_front"),
    path(
        "<slug:store_name>/products/", ProductListView.as_view(), name="store_products"
    ),
    path("<slug:store_name>/user/", UserView.as_view(), name="store_user"),
    path("<slug:store_name>/login/", ClientLoginView.as_view(), name="client_login"),
    path("<slug:store_name>/perfil/", ClientProfileView.as_view(), name="user_profile"),
    path("<slug:store_name>/logout/", StoreLogoutView.as_view(), name="user_logout"),
    path(
        "<slug:store_name>/add-to-cart/<int:product_id>/",
        AddToCartView.as_view(),
        name="add_to_cart",
    ),
    path("<slug:store_name>/cart/", CartView.as_view(), name="user_cart"),
    path(
        "<slug:store_name>/carrinho/remover/<int:item_id>/",
        RemoveFromCartView.as_view(),
        name="remove_from_cart",
    ),
]
