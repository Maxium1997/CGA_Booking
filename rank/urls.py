from django.urls import path, include

from rank.views import ServiceDetailView, MilitaryServiceDetailView
from rank.views import service_addition, branch_addition, military_service_addition, military_branch_addition, rank_addition

urlpatterns = [
    path('service/', include([
        path('detail', ServiceDetailView.as_view(), name='service_detail'),
        path('addition', service_addition, name='service_addition'),
        path('<slug>/', include([
            path('addition', branch_addition, name='branch_addition'),
        ])),
    ])),
    path('military/', include([
        path('service/', include([
            path('detail', MilitaryServiceDetailView.as_view(), name='military_service_detail'),
            path('addition', military_service_addition, name='military_service_addition'),
            path('<slug>/', include([
                path('addition', military_branch_addition, name='military_branch_addition'),
                path('rank/', include([
                    path('addition', rank_addition, name='rank_addition'),
                ]))
            ])),
        ]))
    ]))
]
