from .views import ProfileView, upgrade_me, DownGradeView
from django.contrib.auth.views import LogoutView

from django.urls import path

urlpatterns = [
    path('profile/', ProfileView.as_view(), name="lk-link"),
    path("logout/", LogoutView.as_view(template_name='profile/logout.html'), name="log_out-link"),
    path('downgrade/', DownGradeView.as_view(), name="downgrade-link"),
    path('upgrade/', upgrade_me, name="upgrade-link"),
]
