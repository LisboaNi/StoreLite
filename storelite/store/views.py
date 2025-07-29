from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import FormStore
from django.contrib.auth.models import User, Group


class StoreView(CreateView):
    model = User
    form_class = FormStore
    template_name = "store/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save(commit=False)

        user.is_staff = True
        user.save()

        grupo, criado = Group.objects.get_or_create(name="STORE")
        user.groups.add(grupo)

        self.object = user

        return super().form_valid(form)
