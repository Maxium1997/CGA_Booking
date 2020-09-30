from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView, CreateView, View, DetailView

from registration.models import User, Officer, Education, Work
from registration.definition import Identity
from registration.forms import TravelerRegisterForm, ProprietorRegisterForm, AccountChangeForm
from registration.forms import OfficerForm, AttachmentForm
from registration.forms import EducationForm, WorkForm
from rank.models import Service, Branch, MilitaryService, Rank
from proclamation.models import Proclamation
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

    def get_success_url(self):
        return redirect('user_change')


class ProprietorRegisterView(CreateView):
    model = User
    form_class = ProprietorRegisterForm
    template_name = 'register_info.html'

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return redirect('user_change')

    def get_success_url(self):
        return redirect('user_change')


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'admin/dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['users'] = User.objects.all()
        kwargs['services'] = Service.objects.all()
        kwargs['military_services'] = MilitaryService.objects.all()
        kwargs['proclamations'] = Proclamation.objects.all()
        return super(DashboardView, self).get_context_data(**kwargs)


@method_decorator(login_required, name='dispatch')
class UserDetailView(TemplateView):
    template_name = 'admin/user/detail.html'
    model = User

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, "Permission Denied.")
            return redirect('index')
        return super(UserDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['superusers'] = User.objects.filter(is_superuser=True)
        kwargs['users'] = User.objects.exclude(is_superuser=True)
        kwargs['travelers'] = User.objects.exclude(is_superuser=True).filter(identity=Identity.Traveler.value[0])
        kwargs['proprietors'] = User.objects.exclude(is_superuser=True).filter(identity=Identity.Proprietor.value[0])
        return super(UserDetailView, self).get_context_data(**kwargs)


@login_required
def user_change(request):
    user = request.user
    template = 'account/user_change.html'
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


@method_decorator(login_required, name='dispatch')
class OfficerIndexView(TemplateView):
    template_name = 'account/officer.html'
    model = Officer

    def get_context_data(self, **kwargs):
        try:
            officer = Officer.objects.get(user=self.request.user)
            kwargs['officer'] = officer
            kwargs['officer_form'] = OfficerForm(instance=officer,
                                                 service=self.request.user.officer.service,
                                                 military_service=self.request.user.officer.military_service)
        except:
            new_officer = Officer.objects.create(user=self.request.user)
            kwargs['officer'] = new_officer
            kwargs['officer_form'] = OfficerForm(instance=new_officer)
        kwargs['attachment_of_military_ID_card_front_form'] = AttachmentForm()
        kwargs['attachment_of_military_ID_card_back_form'] = AttachmentForm()
        kwargs['attachment_of_badge_front_form'] = AttachmentForm()
        kwargs['attachment_of_badge_back_form'] = AttachmentForm()
        return super(OfficerIndexView, self).get_context_data(**kwargs)


@login_required
def officer_change(request):
    officer = request.user.officer
    template = 'account/officer.html'
    if request.POST:
        officer_form = OfficerForm(request.POST,
                                   instance=officer,
                                   service=request.user.officer.service,
                                   military_service=request.user.officer.military_service)
        if officer_form.is_valid():
            officer_form.save()
            # messages.success(request, "Officer Change Successfully.")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, "Maybe some data format is invalid, please check again.")
            officer_form = OfficerForm(request.POST,
                                       instance=officer,
                                       service=request.user.officer.service,
                                       military_service=request.user.officer.military_service)
    else:
        officer_form = OfficerForm(instance=officer,
                                   service=request.user.officer.service,
                                   military_service=request.user.officer.military_service)

    context = {'officer_form': officer_form}
    return render(request, template, context)


@login_required
def military_ID_card_front_upload(request):
    officer = request.user.officer
    if request.POST:
        try:
            attachment = AttachmentForm(request.POST, request.FILES)
            officer.attachment_of_military_ID_card_front_upload(attachment['attachment'].data)
            officer.save()
            messages.success(request, "Uploaded Successfully.")
        except AttributeError:
            messages.error(request, "NoneType object has no attribute 'read'.")
        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def military_ID_card_back_upload(request):
    officer = request.user.officer
    if request.POST:
        try:
            attachment = AttachmentForm(request.POST, request.FILES)
            officer.attachment_of_military_ID_card_back_upload(attachment['attachment'].data)
            officer.save()
            messages.success(request, "Uploaded Successfully.")
        except AttributeError:
            messages.error(request, "NoneType object has no attribute 'read'.")
        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def badge_front_upload(request):
    officer = request.user.officer
    if request.POST:
        try:
            attachment = AttachmentForm(request.POST, request.FILES)
            officer.attachment_of_badge_front_upload(attachment['attachment'].data)
            officer.save()
            messages.success(request, "Uploaded Successfully.")
        except AttributeError:
            messages.error(request, "NoneType object has no attribute 'read'.")
        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def badge_back_upload(request):
    officer = request.user.officer
    if request.POST:
        try:
            attachment = AttachmentForm(request.POST, request.FILES)
            officer.attachment_of_badge_back_upload(attachment['attachment'].data)
            officer.save()
            messages.success(request, "Uploaded Successfully.")
        except AttributeError:
            messages.error(request, "NoneType object has no attribute 'read'.")
        return redirect(request.META.get('HTTP_REFERER'))


@method_decorator(login_required, name='dispatch')
class ExperienceIndexView(TemplateView):
    template_name = 'account/experience.html'

    def get_context_data(self, **kwargs):
        kwargs['edu_exps'] = Education.objects.filter(user=self.request.user)
        kwargs['work_exps'] = Work.objects.filter(user=self.request.user)
        kwargs['edu_form'] = EducationForm
        kwargs['work_form'] = WorkForm
        return super(ExperienceIndexView, self).get_context_data(**kwargs)


@login_required
def edu_exp_addition(request):
    user = request.user
    if request.POST:
        edu_form = EducationForm(request.POST)
        if edu_form.is_valid():
            edu_exp = edu_form.save(commit=False)
            edu_exp.user = user
            edu_exp.save()
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            edu_form = EducationForm(request.POST)
            work_form = WorkForm
    else:
        edu_form = EducationForm
        work_form = WorkForm
    context = {'edu_exps': Education.objects.filter(user=user),
               'work_exps': Work.objects.filter(user=user),
               'edu_form': edu_form,
               'work_form': work_form}
    template = 'account/experience.html'
    return render(request, template, context)


@login_required
def work_exp_addition(request):
    user = request.user
    if request.POST:
        work_form = WorkForm(request.POST)
        if work_form.is_valid():
            work_exp = work_form.save(commit=False)
            work_exp.user = user
            work_exp.save()
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            work_form = WorkForm(request.POST)
            edu_form = EducationForm
    else:
        work_form = WorkForm
        edu_form = EducationForm
    context = {'edu_exps': Education.objects.filter(user=user),
               'work_exps': Work.objects.filter(user=user),
               'work_form': work_form,
               'edu_form': edu_form}
    template = 'account/experience.html'
    return render(request, template, context)


@login_required
def edu_exp_delete(request, pk):
    edu_exp = get_object_or_404(Education, pk=pk)
    user = request.user
    if edu_exp.user == user:
        edu_exp.delete()
        messages.success(request, "Delete Successfully.")
    else:
        raise PermissionDenied
    context = {'edu_exps': Education.objects.filter(user=user),
               'work_exps': Work.objects.filter(user=user),
               'edu_form': EducationForm,
               'work_form': WorkForm}
    template = 'account/experience.html'
    return render(request, template, context)


@login_required
def work_exp_delete(request, pk):
    work_exp = get_object_or_404(Work, pk=pk)
    user = request.user
    if work_exp.user == user:
        work_exp.delete()
        messages.success(request, "Delete Successfully.")
    else:
        raise PermissionDenied
    context = {'edu_exps': Education.objects.filter(user=user),
               'work_exps': Work.objects.filter(user=user),
               'edu_form': EducationForm,
               'work_form': WorkForm}
    template = 'account/experience.html'
    return render(request, template, context)
