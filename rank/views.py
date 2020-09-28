from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView, CreateView, View, DetailView
from django.views.generic.edit import UpdateView

from registration.decorator import superuser_check
from rank.models import Service, Branch, MilitaryService, MilitaryBranch, Rank
from rank.forms import ServiceForm, BranchForm, MilitaryServiceForm, MilitaryBranchForm, RankForm

# Create your views here.


@method_decorator(login_required, name='dispatch')
class ServiceDetailView(TemplateView):
    template_name = 'service/index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return super(ServiceDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        context['service_addition_form'] = ServiceForm()
        context['branch_addition_form'] = BranchForm()
        return context


@superuser_check()
def service_addition(request):
    if request.POST:
        service_addition_form = ServiceForm(request.POST)
        if service_addition_form.is_valid():
            try:
                service_addition_form.save()
                messages.success(request, "Added Successfully.")
            except ValueError:
                pass
    return redirect('service_detail')


@superuser_check()
def branch_addition(request, slug):
    service = get_object_or_404(Service, slug=slug)
    if request.POST:
        branch_addition_form = BranchForm(request.POST)
        if branch_addition_form.is_valid():
            try:
                new_branch = branch_addition_form.save(commit=False)
                new_branch.service = service
                new_branch.save()
                messages.success(request, "Added Successfully.")
            except ValueError:
                pass
    return redirect('service_detail')


@method_decorator(login_required, name='dispatch')
class ServiceUpdateView(UpdateView):
    model = Service
    fields = ['name', 'slug']
    template_name = 'service/update.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return super(ServiceUpdateView, self).dispatch(request, *args, **kwargs)


@superuser_check()
def service_delete(request, slug):
    service = get_object_or_404(Service, slug=slug)
    service.delete()
    messages.success(request, "Deleted Successfully.")
    return redirect('service_detail')


@method_decorator(login_required, name='dispatch')
class BranchUpdateView(UpdateView):
    model = Branch
    fields = ['name', 'slug']
    template_name = 'service/branch_update.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return super(BranchUpdateView, self).dispatch(request, *args, **kwargs)


@superuser_check()
def branch_delete(request, slug, pk):
    branch = get_object_or_404(Service, pk=pk)
    branch.delete()
    messages.success(request, "Deleted Successfully.")
    return redirect('service_detail')


@method_decorator(login_required, name='dispatch')
class MilitaryServiceDetailView(TemplateView):
    template_name = 'military/index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return super(MilitaryServiceDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['military_services'] = MilitaryService.objects.all()
        context['military_service_addition_form'] = MilitaryServiceForm()
        context['military_branch_addition_form'] = MilitaryBranchForm()
        context['military_rank_addition_form'] = RankForm()
        return context


@superuser_check()
def military_service_addition(request):
    if request.POST:
        military_service_addition_form = MilitaryServiceForm(request.POST)
        if military_service_addition_form.is_valid():
            try:
                military_service_addition_form.save()
                messages.success(request, "Added Successfully.")
            except ValueError:
                pass
    return redirect('military_service_detail')


@superuser_check()
def military_branch_addition(request, slug):
    military_service = get_object_or_404(MilitaryService, slug=slug)
    if request.POST:
        military_branch_addition_form = MilitaryBranchForm(request.POST)
        if military_branch_addition_form.is_valid():
            try:
                new_branch = military_branch_addition_form.save(commit=False)
                new_branch.military_service = military_service
                new_branch.save()
                messages.success(request, "Added Successfully.")
            except ValueError:
                pass
    return redirect('military_service_detail')


@superuser_check()
def rank_addition(request, slug):
    military_service = get_object_or_404(MilitaryService, slug=slug)
    if request.POST:
        rank_addition_form = RankForm(request.POST)
        if rank_addition_form.is_valid():
            try:
                new_rank = rank_addition_form.save(commit=False)
                new_rank.military_service = military_service
                new_rank.save()
                messages.success(request, "Added Successfully.")
            except ValueError:
                pass
    return redirect('military_service_detail')


@method_decorator(login_required, name='dispatch')
class MilitaryBranchUpdateView(UpdateView):
    model = MilitaryBranch
    fields = ['name', 'slug']
    template_name = 'military/branch_update.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return super(MilitaryBranchUpdateView, self).dispatch(request, *args, **kwargs)


@superuser_check()
def military_branch_delete(request, slug, pk):
    military_branch = get_object_or_404(MilitaryBranch, pk=pk)
    military_branch.delete()
    messages.success(request, "Deleted Successfully.")
    return redirect('military_service_detail')


@method_decorator(login_required, name='dispatch')
class RankUpdateView(UpdateView):
    model = Rank
    fields = ['equivalent_NATO_code', 'name', 'slug']
    template_name = 'military/rank_update.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return super(RankUpdateView, self).dispatch(request, *args, **kwargs)


@superuser_check()
def rank_delete(request, slug, pk):
    rank = get_object_or_404(Rank, pk=pk)
    rank.delete()
    messages.success(request, "Deleted Successfully.")
    return redirect('military_service_detail')
