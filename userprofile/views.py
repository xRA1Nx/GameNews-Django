from GameNewsApp.models import Author, Comment, Post, Category
from users.models import User
import re

from allauth.account.models import EmailAddress
from django.db.models import Q, Count
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView, ListView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from userprofile.filters import CommentsFilter


def profile_edit(request, *args, **kwargs):
    user_id = request.user.id
    action = request.GET.get('profile-action')
    context_dict = {'action': action}

    # удаляем имя
    if action == "del-ava":
        User.objects.all().filter(id=user_id).update(avatar="/static/imgs/ava-default.svg")
        return redirect("/profile/")

    # меняем аву
    if request.method == "POST":
        if action == 'edit-ava':
            new_ava = request.POST.get('ava').strip()
            if not new_ava:
                context_dict['error'] = 'заполните поле'
            else:
                User.objects.all().filter(id=user_id).update(avatar=new_ava)
                return redirect("/profile/")

        # меняем фамилию
        if action == "edit-lname":
            reg_ex = r'^[а-я]+$'
            new_lname = request.POST.get('lname').strip()
            if not new_lname:
                context_dict['error'] = 'заполните поле'
            elif len(new_lname) < 2:
                context_dict['error'] = 'Фамилия д.б. длинее 2х букв'
            elif not re.match(reg_ex, new_lname, flags=re.I):
                context_dict['error'] = 'Фамилия должна состоять только из русских букв'
            else:
                User.objects.all().filter(id=user_id).update(lname=new_lname)
                return redirect("/profile/")

        # меняем имя
        if action == "edit-fname":
            reg_ex = r'^[а-я]+$'
            new_fname = request.POST.get('fname').strip()
            if not new_fname:
                context_dict['error'] = 'заполните поле'
            elif len(new_fname) < 2:
                context_dict['error'] = 'Имя д.б. длинее 2х букв'
            elif not re.match(reg_ex, new_fname, flags=re.I):
                context_dict['error'] = 'Фамилия должна состоять только из русских букв'
            else:
                User.objects.all().filter(id=user_id).update(fname=new_fname)
                return redirect("/profile/")

        # меняем Nick
        if action == "edit-nick":
            new_nick = request.POST.get('nick').strip()
            if not new_nick:
                context_dict['error'] = 'заполните поле'
            elif len(new_nick) < 5:
                context_dict['error'] = 'Ник д.б. длинее 5х символов'
            elif User.objects.all().filter(username__iexact=new_nick.lower()).exists():
                context_dict['error'] = 'Такой ник уже занят'
            else:
                User.objects.all().filter(id=user_id).update(username=new_nick)
                return redirect("/profile/")
        # меняем email
        if action == "edit-email":
            reg_ex = r'^.+@.+$'
            new_email = request.POST.get('email').strip()
            if not new_email:
                context_dict['error'] = 'заполните поле'
            elif len(new_email) < 3:
                context_dict['error'] = 'email д.б. длинее 2х символов'
            elif not re.match(reg_ex, new_email, flags=re.I):
                context_dict['error'] = 'Фамилия должна состоять только из русских букв'
            elif User.objects.all().filter(email__iexact=new_email.lower()).exists():
                context_dict['error'] = 'Такой ник уже занят'
            else:
                User.objects.all().filter(id=user_id).update(email=new_email)
                EmailAddress.objects.all().filter(user_id=user_id).update(email=new_email)
                return redirect("http://127.0.0.1:8000/profile/logout/")

        # # меняем пароль
        # if action == "edit-pass":
        #     new_pass1 = request.POST.get('pass1').strip()
        #     new_pass2 = request.POST.get('pass2').strip()
        #     if not new_pass1:
        #         context_dict['error'] = 'заполните поле'
        #     elif len(new_pass1) < 8:
        #         context_dict['error'] = 'пароль д.б. длинее 7 символов'
        #     elif new_pass1 != new_pass2:
        #         context_dict['error'] = 'Пароли не совпадают'
        #     else:
        #         User.objects.all().filter(id=user_id)[0].set_password(new_pass1)
        #         return redirect("http://127.0.0.1:8000/profile/logout/")

    return render(request, 'profile/profile-edit.html', context=context_dict)


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
    com = Comment.objects.filter(pk=int(com_id))
    com.update(accepted=True)
    com[0].save()
    return redirect("/profile/confirm-comments/")
