from django.urls import path, include

from django.contrib.auth.views import LoginView, LogoutView

from registration.views import RegisterView, TravelerRegisterView, ProprietorRegisterView

urlpatterns = [
    path('accounts/', include([
        path('register', RegisterView.as_view(), name='register'),
        path('register/', include([
            path('traveler', TravelerRegisterView.as_view(), name='traveler_register'),
            path('proprietor', ProprietorRegisterView.as_view(), name='proprietor_register'),
        ])),
        path('login', LoginView.as_view(template_name='login.html'), name='login'),
        path('logout', LogoutView.as_view(), name='logout'),
    ]))
]
