from django.contrib import admin
from .models import Store, UserProfile

from django.utils.html import format_html


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    fields = (
        "store",
        "cnpj",
        "logo",
        "page",
        "main",
        "draft",
        "text",
        "telephone",
        "whatsapp",
        "email",
        "store_link",
    )
    readonly_fields = ("user", "layout", "slug", "store_link")

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
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        exists = Store.objects.filter(user=request.user).exists()
        return not exists

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or (obj and obj.user == request.user):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

    @admin.display(description="Store link")
    def store_link(self, obj):
        if obj.store:
            url = obj.get_store_url()
            return format_html('<a href="{}" target="_blank">Access the store</a>', url)
        return "-"


admin.site.register(UserProfile)
