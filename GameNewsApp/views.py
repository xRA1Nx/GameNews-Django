from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .models import Post, Author, Category
from .forms import PostAddForm, CommentAddForm
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.db.models import Count, Q, Case, When


@login_required
def subscribe(request, *args, **kwargs):
    context_dict = {}
    subscribed = request.user.category_set.all()
    context_dict['subscribed'] = subscribed

    if request.method == 'POST':

        if request.POST['action'] == 'subscibe':
            post_id = request.POST['post_id']
            post = Post.objects.get(pk=post_id)
            user = request.user
            for cat in post.categorys.all():
                if user not in cat.subsribers.all():
                    cat.subsribers.add(request.user)
        elif request.POST['action'] == 'unsubscibe':
            cat_id = request.POST['category']
            cat_obj = Category.objects.get(pk=cat_id)
            user = request.user
            cat_obj.subsribers.remove(user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # return render(request, 'profile/lk.html', context=context_dict)


def news_search(request, *args, **kwargs):
    context_dict = {}

    if request.method == "POST":
        text = request.POST['text']
        news = Post.objects.all().filter(Q(title__icontains=text) | Q(description__icontains=text) | Q(
            text__icontains=text)).annotate(
            count_comments=Count(Case(When(
                comment__accepted=True, then=1)))).order_by(
            '-date_time')

        #
        # p = Paginator(news, 2)
        # res = p.get_page(request.GET.get('page', 1))
        context_dict['news'] = news
        context_dict['aside_posts'] = Post.objects.annotate(
            count_comments=Count(Case(When(
                comment__accepted=True, then=1)))).order_by(
            '-count_comments')[0:3]
        context_dict['nums'] = [1, 2, 3]
        return render(request, 'search.html', context=context_dict)
    else:
        return redirect('/')


# class NewsSearchView(ListView):
#     model = Post
#     context_object_name = 'news'
#     template_name = 'search.html'
#     ordering = '-date_time'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['aside_posts'] = Post.objects.annotate(count_comments=Count('comment')).order_by(
#             '-count_comments')[0:3]
#         context['nums'] = [1, 2, 3]
#         context['filter'] = SearchNewsFilter(self.request.GET,
#                                        queryset=self.get_queryset())  # вписываем наш фильтр в контекст
#
#         return context


class CategoryFilter(ListView):
    model = Post
    context_object_name = 'news'
    template_name = 'filter.html'
    ordering = '-date_time'
    paginate_by = 9

    def get_queryset(self):
        qs = Post.objects.annotate(
            count_comments=Count(Case(When(
                comment__accepted=True, then=1)))).order_by(
            '-date_time')

        # если метод POST - фильтруем по поиску
        if self.request.method == 'POST':
            return qs
        else:  # если метод GET
            query = self.request.GET.get('category')  # берем категорию из гет запроса
            if not query:  # если в запросе нет категории
                return qs  # возвращаем первичный qs
            return qs.filter(categorys__name__contains=query)  # возвращем qs отфильтрованный по категориям

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aside_posts'] = Post.objects.annotate(
            count_comments=Count(Case(When(
                comment__accepted=True, then=1)))).order_by(
            '-count_comments')[0:3]
        if self.request.GET.get('category'):
            context['category'] = self.request.GET.get('category')
        context['nums'] = [1, 2, 3]
        return context


class NewsView(ListView):
    model = Post
    context_object_name = 'news'
    template_name = 'news.html'
    paginate_by = 9

    def get_queryset(self):
        return Post.objects.annotate(
            count_comments=Count(Case(When(
                comment__accepted=True, then=1)))).order_by(
            '-date_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aside_posts'] = Post.objects.annotate(
            count_comments=Count(Case(When(
                comment__accepted=True, then=1)))).order_by(
            '-count_comments')[0:3]
        context['nums'] = [1, 2, 3]
        return context


class PostView(FormMixin, DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post.html'
    form_class = CommentAddForm

    # def get_initial(self):
    #     initial = super().get_initial()
    #     user = self.request.user
    #     initial['user'] = user
    #     initial['post'] = self.object
    #
    #     return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # исправить, пройтись циклом
        context['comment_count'] = Post.objects.filter(id=self.object.id).annotate(
            count_comments=Count(Case(When(
                comment__accepted=True, then=1))))[0].count_comments
        post_text = self.object.text.split("\n")
        # post_text = self.object.text
        context['post_text'] = post_text
        context['aside_posts'] = Post.objects.annotate(
            count_comments=Count(Case(When(
                comment__accepted=True, then=1)))).order_by('-count_comments')[0:3]
        context['post_comments'] = self.object.comment_set.all().order_by('-date_time')
        flag = False
        for cat in context['post'].categorys.all():
            if self.request.user in cat.subsribers.all():
                flag = True
                break
        context['user_is_subscribed'] = flag
        return context

    def get_success_url(self):
        return reverse('post-link', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(PostView, self).form_valid(form)


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = "GameNewsApp.add_post"
    context_object_name = 'post'
    template_name = 'post_add.html'
    form_class = PostAddForm

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        author = Author.objects.get(user_id=user.pk)
        initial['author'] = author
        return initial


class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = "GameNewsApp.change_post"
    model = Post
    context_object_name = 'post'
    template_name = "post_add.html"
    form_class = PostAddForm


class PostDel(PermissionRequiredMixin, DeleteView):
    permission_required = "GameNewsApp.delete_post"
    model = Post
    context_object_name = 'post'
    template_name = "post_del.html"
    success_url = 'http://127.0.0.1:8000/'


class CommentAdd(CreateView):
    form_class = CommentAddForm
    context_object_name = 'comment'
    template_name = 'comment-add.html'

    def get_success_url(self):
        res = f"http://127.0.0.1:8000/{self.request.GET.get('post_id')}#comment-{self.object.id}"
        return res

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial['user'] = user
        initial['post'] = self.request.GET.get('post_id')
        return initial
