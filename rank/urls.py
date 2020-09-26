from django.urls import path, include

from rank.views import ServiceDetailView, MilitaryServiceDetailView, ServiceUpdateView, BranchUpdateView, MilitaryBranchUpdateView, RankUpdateView
from rank.views import service_addition, branch_addition, military_service_addition, military_branch_addition, rank_addition
from rank.views import service_delete, branch_delete, military_branch_delete, rank_delete

urlpatterns = [
    path('service/', include([
        path('detail', ServiceDetailView.as_view(), name='service_detail'),
        path('addition', service_addition, name='service_addition'),
        path('<slug>/', include([
            path('addition', branch_addition, name='branch_addition'),
            path('update', ServiceUpdateView.as_view(), name='service_update'),
            path('delete', service_delete, name='service_delete'),
            path('branch/', include([
                path('<pk>/', include([
                    path('update', BranchUpdateView.as_view(), name='branch_update'),
                    path('delete', branch_delete, name='branch_delete'),
                ]))
            ]))
        ])),
    ])),
    path('military/', include([
        path('service/', include([
            path('detail', MilitaryServiceDetailView.as_view(), name='military_service_detail'),
            path('addition', military_service_addition, name='military_service_addition'),
            path('<slug>/', include([
                path('branch/', include([
                    path('addition', military_branch_addition, name='military_branch_addition'),
                    path('<pk>/', include([
                        path('update', MilitaryBranchUpdateView.as_view(), name='military_branch_update'),
                        path('delete', military_branch_delete, name='military_branch_delete'),
                    ]))
                ])),
                path('rank/', include([
                    path('addition', rank_addition, name='rank_addition'),
                    path('<pk>/', include([
                        path('update', RankUpdateView.as_view(), name='rank_update'),
                        path('delete', rank_delete, name='rank_delete'),
                    ]))
                ])),
            ])),
        ])),
    ]))
]
