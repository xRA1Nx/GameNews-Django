from .models import Post
from .forms import PostAddForm, CommentAddForm

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Count

class CategoryFilter(ListView):
    model = Post
    context_object_name = 'news'
    template_name = 'filter.html'
    ordering = '-date_time'


class NewsView(ListView):
    model = Post
    context_object_name = 'news'
    template_name = 'news.html'
    ordering = '-date_time'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aside_posts'] = Post.objects.annotate(count_comments=Count('comment')).order_by(
            '-count_comments')[0:3]
        return context


class PostView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aside_posts'] = Post.objects.annotate(count_comments=Count('comment')).order_by(
            '-count_comments')[0:3]
        return context


class PostCreate(CreateView):
    context_object_name = 'post'
    template_name = 'post_add.html'
    form_class = PostAddForm

    # def get_initial(self):
    #     initial = super().get_initial()
    #     user = self.request.user
    #     author = Author.objects.get(user_id=user.pk)
    #     initial['author'] = author
    #     return initial


class PostEdit(UpdateView):
    model = Post
    context_object_name = 'post'
    template_name = "post_add.html"
    form_class = PostAddForm


class PostDel(DeleteView):
    model = Post
    context_object_name = 'post'
    template_name = "post_del.html"
    success_url = 'http://127.0.0.1:8000/news/'


class CommentAdd(CreateView):
    context_object_name = 'post'
    template_name = 'post.html'
    form_class = CommentAddForm
