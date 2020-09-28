from django.urls import path, include

from .views import ProclamationIndexView, ProclamationCreateView, ProclamationDetailView, ProclamationUpdateView

urlpatterns = [
    path('proclamation/', include([
        path('index', ProclamationIndexView.as_view(), name='proclamation_index'),
        path('creation', ProclamationCreateView.as_view(), name='proclamation_creation'),
        path('<pk>/', include([
            path('detail', ProclamationDetailView.as_view(), name='proclamation_detail'),
            path('update', ProclamationUpdateView.as_view(), name='proclamation_update'),
        ])),
    ]))
]