from django.shortcuts import render, redirect
from django.contrib import auth
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


class DashboardView(View):
    pass
