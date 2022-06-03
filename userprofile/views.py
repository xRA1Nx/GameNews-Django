from django.db.models import Q, Count

from GameNewsApp.models import Author, Comment, Post, Category

from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView, ListView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from userprofile.filters import CommentsFilter


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile/lk.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subscribed = self.request.user.category_set.all()
        context['subscribed'] = subscribed
        context["premium"] = self.request.user.groups.filter(name="author").exists()
        return context


class AuthorComments(LoginRequiredMixin, ListView):
    template_name = 'profile/user-comments.html'
    context_object_name = 'comments'
    model = Comment
    # model = Post
    # queryset = Post.objects.order_by("-date_time")
    paginate_by = 5

    def get_context_data(self,
                         **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = CommentsFilter(self.request.GET,
                                           queryset=self.get_queryset())
        return context

    def get_queryset(self):
        posts = Post.objects.filter(author__user__id=self.request.user.id).values("id")
        comms = Comment.objects.filter(Q(post__id__in=posts) & Q(accepted=False))
        return CommentsFilter(self.request.GET, queryset=comms).qs


@login_required
def upgrade_me(request):
    current_user = request.user
    premium_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        premium_group.user_set.add(current_user)
    if not Author.objects.filter(user_id=int(current_user.pk)).exists():
        Author.objects.create(user_id=int(current_user.pk))
    return redirect('/profile/')


class DownGradeView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/lk.html'

    def get(self, request, *args, **kwargs):
        current_user = request.user
        premium_group = Group.objects.get(name='author')
        if request.user.groups.filter(name='author').exists():
            premium_group.user_set.remove(current_user)
        Author.objects.filter(user_id=int(current_user.pk)).delete()
        return redirect("/profile/")


def comment_del(request, *args, **kwargs):
    com_id = request.POST['comment-id']
    Comment.objects.filter(pk=int(com_id)).delete()
    return redirect("/profile/confirm-comments/")


def comment_accept(request, *args, **kwargs):
    com_id = request.POST['comment-id']
    Comment.objects.filter(pk=int(com_id)).update(accepted=True)
    return redirect("/profile/confirm-comments/")
