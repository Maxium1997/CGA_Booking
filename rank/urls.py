from django.urls import path, include

from rank.views import ServiceDetailView

urlpatterns = [
    path('service/', include([
        path('detail', ServiceDetailView.as_view(), name='service_detail'),
    ])),
]
