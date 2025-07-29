from django.contrib import admin
from .models import Product, CartItem
from store.models import Store


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ("name", "description", "photo", "cost", "stock", "number", "size")
    readonly_fields = ("user", "store")

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        return self.readonly_fields

    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return [field.name for field in self.model._meta.fields]
        return self.fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
            try:
                obj.store = Store.objects.get(user=request.user)
            except Store.DoesNotExist:
                self.message_user(
                    request, "Nenhuma loja associada ao usuário.", level="error"
                )
                return
        super().save_model(request, obj, form, change)


admin.site.register(CartItem)
