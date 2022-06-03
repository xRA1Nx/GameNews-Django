from django.db import models
from django.contrib.auth.models import AbstractBaseUser, User
from django.utils.translation import gettext_lazy as _


class PortalUser(AbstractBaseUser):
    avatar = models.TextField(max_length=500, default='/static/imgs/ava-default.svg')
    fname = models.TextField(max_length=50, blank=True)
    lname = models.TextField(max_length=50, blank=True)
    email = models.TextField(max_length=100, unique=True,
                             error_messages={
                                 'unique': _("A user with that username already exists."),
                             },
                             )
    username = models.TextField(max_length=50, unique=True, default=email)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    subsribers = models.ManyToManyField(User, through='UserCategory')

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categorys = models.ManyToManyField(Category, through='PostCategory')
    date_time = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=80)
    description = models.TextField(max_length=320)
    text = models.TextField()
    main_img = models.TextField(max_length=500)
    small_img = models.TextField(max_length=500)

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/{self.id}'

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    date_time = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)


class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
