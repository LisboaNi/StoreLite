# store/views.py
from django.views import View
from django.views.generic import TemplateView, DetailView

from store.models import Store, UserProfile
from product.models import Product, CartItem

from django.http import Http404

from django.urls import reverse_lazy, reverse
from .forms import FormUser

from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect


class StoreFrontView(TemplateView):
    template_name = "public/public.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        store_slug = self.kwargs.get("store_name")

        try:
            store = Store.objects.get(slug=store_slug)
        except Store.DoesNotExist:
            raise Http404("Loja não encontrada")

        products = Product.objects.filter(store=store)
        context["store"] = store
        context["products"] = products
        return context


class ProductListView(DetailView):
    model = Store
    template_name = "public/product.html"
    context_object_name = "store"
    slug_field = "slug"
    slug_url_kwarg = "store_name"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        store = self.get_object()
        context["products"] = store.products.all()
        return context


class UserView(CreateView):
    model = User
    form_class = FormUser
    template_name = "public/user.html"
    success_url = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        self.store = get_object_or_404(Store, slug=self.kwargs["store_name"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        store = get_object_or_404(Store, slug=self.kwargs["store_name"])
        context["store"] = store
        return context

    def form_valid(self, form):
        user = form.save(commit=False)

        user.is_staff = False
        user.is_superuser = False
        user.save()

        UserProfile.objects.create(user=user, email=user.email, store=self.store)

        return super().form_valid(form)


class ClientLoginView(LoginView):
    template_name = "public/login.html"
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        store = get_object_or_404(Store, slug=self.kwargs["store_name"])
        context["store"] = store
        return context

    def get_success_url(self):
        user = self.request.user
        profile = UserProfile.objects.get(user=user)
        return reverse("public:store_front", kwargs={"store_name": profile.store.slug})


class ClientProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = "public/profile.html"
    fields = ["telephone", "email"]

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["store"] = get_object_or_404(Store, slug=self.kwargs["store_name"])
        context["user"] = self.request.user
        return context

    def form_valid(self, form):
        user = self.request.user
        user.email = self.request.POST.get("email", user.email)
        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "public:user_profile", kwargs={"store_name": self.kwargs["store_name"]}
        )


class StoreLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        self.store_name_from_url = kwargs.get("store_name")
        response = super().dispatch(request, *args, **kwargs)

        if isinstance(response, HttpResponseRedirect):
            return response

        next_page = self.get_next_page()
        if next_page:
            return redirect(next_page)

        return redirect("/")

    def get_next_page(self):
        store_slug = self.store_name_from_url
        return reverse("public:store_front", kwargs={"store_name": store_slug})


class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, store_name, product_id):
        store = get_object_or_404(Store, slug=store_name)
        product = get_object_or_404(Product, id=product_id, store=store)

        if product.stock < 1:
            # Pode mostrar uma mensagem se quiser, mas aqui só redireciona
            return redirect("public:store_products", store_name=store.slug)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, product=product, store=store
        )
        if not created:
            cart_item.quantity += 1
        else:
            cart_item.quantity = 1

        cart_item.save()

        product.stock -= 1
        product.save()

        return redirect("public:store_products", store_name=store.slug)


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, store_name, item_id):
        store = get_object_or_404(Store, slug=store_name)
        cart_item = get_object_or_404(
            CartItem, id=item_id, user=request.user, store=store
        )

        cart_item.product.stock += 1
        cart_item.product.save()

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

        return redirect("public:user_cart", store_name=store.slug)


class CartView(LoginRequiredMixin, TemplateView):
    template_name = "public/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        store = get_object_or_404(Store, slug=self.kwargs["store_name"])
        cart_items = CartItem.objects.filter(user=self.request.user, store=store)

        total = sum(item.product.cost * item.quantity for item in cart_items)

        context["store"] = store
        context["cart_items"] = cart_items
        context["total"] = total
        return context
