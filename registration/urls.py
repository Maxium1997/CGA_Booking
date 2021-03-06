from django.urls import path, include

from django.contrib.auth.views import LoginView, LogoutView

from registration.views import DashboardView, UserDetailView
from registration.views import RegisterView, TravelerRegisterView, ProprietorRegisterView
from registration.views import user_change
from registration.views import OfficerIndexView
from registration.views import officer_change, military_ID_card_front_upload, military_ID_card_back_upload, \
    badge_front_upload, badge_back_upload
from registration.models import Education, Work
from registration.views import ExperienceIndexView
from registration.views import edu_exp_addition, work_exp_addition, edu_exp_delete, work_exp_delete

urlpatterns = [
    path('admin/', include([
        path('dashboard', DashboardView.as_view(), name='dashboard'),
        path('dashboard/', include([
            path('', include('proclamation.urls'))
        ])),
        path('users', UserDetailView.as_view(), name='user_detail'),
        path('', include('rank.urls'))
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

        path('officer/', include([
            path('index', OfficerIndexView.as_view(), name='officer_index'),
            path('change', officer_change, name='officer_change'),
            path('change/', include([
                path('military_ID_card/', include([
                    path('front', military_ID_card_front_upload, name='military_ID_card_front_upload'),
                    path('back', military_ID_card_back_upload, name='military_ID_card_back_upload'),
                ])),
                path('badge/', include([
                    path('front', badge_front_upload, name='badge_front_upload'),
                    path('back', badge_back_upload, name='badge_back_upload'),
                ])),
            ])),
        ])),

        path('experience/', include([
            path('index', ExperienceIndexView.as_view(), name='experience_index'),
            path('education/', include([
                path('addition', edu_exp_addition, name='edu_exp_addition'),
                path('<pk>/', include([
                    path('delete', edu_exp_delete, name='edu_exp_delete')
                ]))
            ])),
            path('work/', include([
                path('addition', work_exp_addition, name='work_exp_addition'),
                path('<pk>/', include([
                    path('delete', work_exp_delete, name='work_exp_delete')
                ]))
            ]))
        ])),
    ])),
]
