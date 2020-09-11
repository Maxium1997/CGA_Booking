from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView, CreateView, View, DetailView

from rank.models import Service, Branch, Rank
from rank.forms import ServiceForm

# Create your views here.


@method_decorator(login_required, name='dispatch')
class ServiceDetailView(TemplateView):
    template_name = 'admin/service/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        context['service_addition_form'] = ServiceForm()
        return context

    def post(self, request):
        if request.user.is_superuser:
            if request.POST:
                service_addition_form = ServiceForm(request.POST)
                if service_addition_form.is_valid():
                    service_addition_form.save()
                    messages.success(request, "Added Successfully.")
                # else:
                #     context = {'services': Service.objects.all(),
                #                'service_addition_form': ServiceForm(request.POST)}
                #     template = 'admin/service/detail.html'
        else:
            messages.error(request, "Permission Denied.")
        return redirect(request.META.get('HTTP_REFERER'))
