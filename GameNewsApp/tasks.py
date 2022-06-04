
from celery import shared_task
import datetime
from .models import Post, Category
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from time import sleep




@shared_task
def printer(n):
    for i in range(n):
        sleep(1)
        print(i + 1)


@shared_task
def hello():
    sleep(3)
    print("Hello, world!")


# @shared_task
# def celery_notify_subscribers(my_pk):
#     instance = Post.objects.get(pk=my_pk)
#     html_content = render_to_string('email/send_on_create.html', {'my_post': instance}, )
#     cats = instance.categorys.all()
#     sendto_set = set()
#     for cat in cats:
#         sendto_set |= cat.get_subscribers_emails()
#     msg = EmailMultiAlternatives(
#         subject=f'"Здравствуйте, {instance.author.user} CELERY рассылка!!!"',
#         body=instance.text,
#         from_email='stwski@inbox.ru',
#         to=sendto_set)
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()


@shared_task
def celery_every_week_notify():
    delta = datetime.timedelta(7)
    start_date = datetime.datetime.utcnow() - delta
    end_date = datetime.datetime.utcnow()
    posts_for_week_send = Post.objects.filter(time_in__range=(start_date, end_date))

    for cat in Category.objects.all():
        html_content = render_to_string('email/evere_week_send.html', {'posts': posts_for_week_send, 'cat': cat}, )
        msg = EmailMultiAlternatives(
            subject=f'"Ваша подписка на GameNews. Еженедельная рассылка от CELERY"',
            from_email='stwski@inbox.ru',
            to=cat.get_subscribers_emails())
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    print("письмо отправлено")
