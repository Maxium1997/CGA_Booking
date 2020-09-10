from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView, CreateView, View, DetailView

from registration.models import User
from registration.definition import Identity
from registration.forms import TravelerRegisterForm, ProprietorRegisterForm, AccountChangeForm
from rank.models import Service, Branch, Rank
# from rank.forms import RankForm
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
        return redirect('user_change')


class ProprietorRegisterView(CreateView):
    model = User
    form_class = ProprietorRegisterForm
    template_name = 'register_info.html'

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return redirect('user_change')


@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        template = 'admin/dashboard.html'
        context = {'users': User.objects.all(),
                   # 'travelers': User.objects.filter(identity=Identity.Traveler.value[0]),
                   # 'proprietors': User.objects.filter(identity=Identity.Proprietor.value[0]),
                   'services': Service.objects.all(),
                   'branches': Branch.objects.all(),
                   'ranks': Rank.objects.all()}

        return render(request, template, context)


@method_decorator(login_required, name='dispatch')
class UserDetailView(TemplateView):
    template_name = 'admin/user/detail.html'
    model = User

    def get_context_data(self, **kwargs):
        kwargs['superusers'] = User.objects.filter(is_superuser=True)
        kwargs['users'] = User.objects.exclude(is_superuser=True)
        kwargs['travelers'] = User.objects.exclude(is_superuser=True).filter(identity=Identity.Traveler.value[0])
        kwargs['proprietors'] = User.objects.exclude(is_superuser=True).filter(identity=Identity.Proprietor.value[0])
        return super(UserDetailView, self).get_context_data(**kwargs)
        # context = super().get_context_data(**kwargs)
        # context['superusers'] = User.objects.filter(is_superuser=True)
        # context['users'] = User.objects.exclude(is_superuser=True)
        # context['travelers'] = User.objects.exclude(is_superuser=True).filter(identity=Identity.Traveler.value[0])
        # context['proprietors'] = User.objects.exclude(is_superuser=True).filter(identity=Identity.Proprietor.value[0])
        # return context


@login_required
def user_change(request):
    user = request.user
    template = 'user_change.html'
    if request.POST:
        user_change_form = AccountChangeForm(request.POST, instance=user)
        if user_change_form.is_valid():
            user_change_form.save()
            messages.success(request, "User Change Successfully.")
            return redirect('index')
        else:
            messages.warning(request, "Maybe some data format is invalid, please check again.")
            user_change_form = AccountChangeForm(request.POST, instance=user)
    else:
        user_change_form = AccountChangeForm(instance=user)

    context = {'account_change_form': user_change_form}
    return render(request, template, context)
