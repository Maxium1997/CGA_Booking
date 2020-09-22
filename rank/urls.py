from django.urls import path, include

from rank.views import ServiceDetailView
from rank.views import service_addition, branch_addition

urlpatterns = [
    path('service/', include([
        path('detail', ServiceDetailView.as_view(), name='service_detail'),
        path('addition', service_addition, name='service_addition'),
        path('<slug>/', include([
            path('addition', branch_addition, name='branch_addition'),
        ])),
    ])),
]
