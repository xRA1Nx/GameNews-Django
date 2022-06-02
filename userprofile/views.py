from GameNewsApp.models import Author

from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect

from django.contrib.auth.mixins import LoginRequiredMixin


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile/lk.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["premium"] = self.request.user.groups.filter(name="author").exists()
        return context


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
