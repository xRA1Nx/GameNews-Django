from .views import ProfileView, upgrade_me, DownGradeView, AuthorComments, comment_del, comment_accept
from django.contrib.auth.views import LogoutView

from django.urls import path

urlpatterns = [
    path('', ProfileView.as_view(), name="lk-link"),
    path("logout/", LogoutView.as_view(), name="log_out-link"),
    path('downgrade/', DownGradeView.as_view(), name="downgrade-link"),
    path('upgrade/', upgrade_me, name="upgrade-link"),
    path('confirm-comments/', AuthorComments.as_view(), name='confirm-comments-link'),
    path('comment-del/', comment_del, name="comment-del-link"),
    path('comment-accept/', comment_accept, name="comment-accept-link"),
]
