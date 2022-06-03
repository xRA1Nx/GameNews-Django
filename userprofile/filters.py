from django.forms import DateInput, TextInput, Select
from django_filters import FilterSet, DateFilter, CharFilter, ChoiceFilter
from GameNewsApp.models import Comment


class CommentsFilter(FilterSet):
    date_time = DateFilter(
        field_name='date_time',
        lookup_expr='gt',
        label='Опубликовано после ',
        widget=DateInput(
            format='%d.%m.%Y',
            attrs={'type': 'date', 'class': 'inp'}))

    post__title = CharFilter(
        label='название новости',
        lookup_expr='icontains',
        widget=TextInput(attrs={'class': 'inp'}))

    post__categorys = ChoiceFilter(
        label='категории',
        choices=[
            (1, 'Diablo'),
            (2, 'Overwatch'),
            (3, 'HoS'),
            (4, 'Starcraft'),
            (5, 'Hearthstone'),
            (6, 'Warcraft'),
            (7, 'Другие игры'),
        ],
        widget=Select(attrs={'class': 'inp'}))

    class Meta:
        model = Comment
        fields = ['post__title', 'date_time', 'post__categorys']

# , 'post__categorys'
