from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView, CreateView, View

from registration.models import User
from registration.forms import TravelerRegisterForm, ProprietorRegisterForm
# Create your views here.


class RegisterView(TemplateView):
    template_name = 'register.html'


class TravelerRegisterView(CreateView):
    model = User
    form_class = TravelerRegisterForm
    template_name = 'register_info.html'

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return redirect('index')


class ProprietorRegisterView(CreateView):
    model = User
    form_class = ProprietorRegisterForm
    template_name = 'register_info.html'

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return redirect('index')


@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        template = 'admin/dashboard.html'
        context = {'users': User.objects.all()}

        return render(request, template, context)
