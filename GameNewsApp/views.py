from .models import Post, Author
from .forms import PostAddForm, CommentAddForm
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.db.models import Count


class CategoryFilter(ListView):
    model = Post
    context_object_name = 'news'
    template_name = 'filter.html'
    ordering = '-date_time'

    def get_queryset(self):
        qs = super(CategoryFilter, self).get_queryset()

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
        context['aside_posts'] = Post.objects.annotate(count_comments=Count('comment')).order_by(
            '-count_comments')[0:3]
        context['nums'] = [1, 2, 3]
        return context


class NewsView(ListView):
    model = Post
    context_object_name = 'news'
    template_name = 'news.html'
    ordering = '-date_time'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aside_posts'] = Post.objects.annotate(count_comments=Count('comment')).order_by(
            '-count_comments')[0:3]
        context['nums'] = [1, 2, 3]
        return context


class PostView(FormMixin, DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post.html'
    form_class = CommentAddForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aside_posts'] = Post.objects.annotate(count_comments=Count('comment')).order_by(
            '-count_comments')[0:3]
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
    success_url = 'http://127.0.0.1:8000/news/'
