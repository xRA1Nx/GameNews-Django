from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    subsribers = models.ManyToManyField(User, through='UserCategory')


class Post(models.Model):
    id_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')
    date_time = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=80)
    description = models.CharField(max_length=320)
    main_img = models.CharField(max_length=500)
    small_img = models.CharField(max_length=500)


class Comment(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_news = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)


class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
