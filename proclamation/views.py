from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied

from registration.models import User
from proclamation.models import Proclamation
from proclamation.forms import ProclamationForm
# Create your views here.


@method_decorator(login_required, name='dispatch')
class ProclamationIndexView(TemplateView):
    template_name = 'proclamation/index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return super(ProclamationIndexView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProclamationIndexView, self).get_context_data(**kwargs)
        context['proclamations'] = Proclamation.objects.all()
        return context


@method_decorator(login_required, name='dispatch')
class ProclamationCreateView(TemplateView):
    model = Proclamation
    template_name = 'proclamation/creation.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return super(ProclamationCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['form'] = ProclamationForm()
        return super(ProclamationCreateView, self).get_context_data(**kwargs)

    def post(self, request):
        if request.user.is_superuser:
            ProclamationForm(request.POST).save(announcer=request.user)
            return redirect('proclamation_index')
        else:
            raise PermissionDenied


class ProclamationDetailView(DetailView):
    model = Proclamation
    template_name = 'proclamation/detail.html'


@method_decorator(login_required, name='dispatch')
class ProclamationUpdateView(UpdateView):
    model = Proclamation
    template_name = 'proclamation/update.html'
    fields = ['title', 'content']

    def get_context_data(self, **kwargs):
        obj = super(ProclamationUpdateView, self).get_object()
        kwargs['form'] = ProclamationForm(instance=obj)
        return super(ProclamationUpdateView, self).get_context_data(**kwargs)
