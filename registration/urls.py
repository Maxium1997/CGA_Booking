from django.urls import path, include

from registration.views import RegisterView

urlpatterns = [
    path('accounts/', include([
        path('register', RegisterView.as_view(), name='register'),
        # path('login', ),
        # path('logout', ),
    ]))
]
