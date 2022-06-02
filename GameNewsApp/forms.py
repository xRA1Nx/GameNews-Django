from .models import Post, Comment

from django.forms import ModelForm, CharField, Textarea, MultipleChoiceField, HiddenInput, TextInput, URLInput, \
    SelectMultiple, IntegerField


class PostAddForm(ModelForm):
    # obj_list = list(Category.objects.all().values('pk', 'name'))
    # choise_list = [(list(obj_list[i].values())[0], list(obj_list[i].values())[1]) for i in range(len(obj_list))]

    categorys = MultipleChoiceField(
        label="категории",
        # choices=choise_list,

        choices=[
            (1, 'Diablo'),
            (2, 'Overwatch'),
            (3, 'HoS'),
            (4, 'Starcraft'),
            (5, 'Hearthstone'),
            (6, 'Warcraft'),
            (7, 'Другие игры'),
        ],

        widget=SelectMultiple(attrs={
            'placeholder': "выберите категорию",
            'class': "inp",
            'size': 7
        }))

    main_img = CharField(
        label="основная картинка",
        widget=URLInput(attrs={
            'placeholder': "ссылка на вашу картинку",
            # 'class': "inp",
        }))

    small_img = CharField(
        label="маленькая картинка",
        widget=URLInput(attrs={
            'placeholder': "ссылка на вашу картинку",
            # 'class': "inp",
        }))
    title = CharField(
        label='заголовок',
        widget=TextInput(attrs={
            'placeholder': "введите заголовок",
            'class': "inp",
        }))
    description = CharField(
        label='Краткое описание:',
        widget=Textarea(attrs={
            'placeholder': "введите заголовок",
            'class': "inp post-preview-ta",
        }))
    text = CharField(
        label='Текст статьи:',
        widget=Textarea(attrs={
            'placeholder': "напишите статью",
            'class': "inp post-ta",
        }))

    class Meta:
        model = Post
        fields = ['categorys', 'main_img', 'small_img', 'title', 'description', 'text', 'author']

        labels = {
            'categorys': "категории",
            # 'main_img': 'основная картинка',
            # 'small_img': 'маленькая картинка',
            # 'title': 'заголовок',
            # 'description': 'краткое описание',
            # 'text': 'Статья'
        }

        widgets = {
            'author': HiddenInput(),
        }


class CommentAddForm(ModelForm):
    text = CharField(label="Статья", min_length=3, widget=Textarea)

    class Meta:
        model = Comment
        fields = ['text', "post", 'user']
