from .views import NewsView, PostView, PostCreate, PostEdit, \
    PostDel, CategoryFilter, CommentAdd, subscribe

from django.urls import path

urlpatterns = [
    path('', NewsView.as_view(), name='news-link'),
    path('filtred/', CategoryFilter.as_view(), name='filter-link'),
    path('<int:pk>/', PostView.as_view(), name='post-link'),
    path('post-add/', PostCreate.as_view(), name='post-add-link'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post-edit-link'),
    path('<int:pk>/del/', PostDel.as_view(), name='post-del-link'),
    path('comment-add/', CommentAdd.as_view(), name='comment-add-link'),
    path('subscriptions/', subscribe, name='subscriptions'),
    # path('<int:pk>/', CommentAdd.as_view(), name='post-add-link'),
]
