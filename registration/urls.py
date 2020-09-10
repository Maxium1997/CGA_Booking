from django.urls import path, include

from django.contrib.auth.views import LoginView, LogoutView

from registration.views import DashboardView, UserDetailView
from registration.views import RegisterView, TravelerRegisterView, ProprietorRegisterView
from registration.views import user_change

urlpatterns = [
    path('admin/', include([
        path('dashboard', DashboardView.as_view(), name='dashboard'),
        path('users', UserDetailView.as_view(), name='user_detail'),
    ])),

    path('accounts/', include([
        path('register', RegisterView.as_view(), name='register'),
        path('register/', include([
            path('traveler', TravelerRegisterView.as_view(), name='traveler_register'),
            path('proprietor', ProprietorRegisterView.as_view(), name='proprietor_register'),
        ])),
        path('login', LoginView.as_view(template_name='login.html'), name='login'),
        path('logout', LogoutView.as_view(), name='logout'),
        path('change', user_change, name='user_change'),
    ]))
]
