from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import User, Comment
from django.dispatch import receiver

from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import Group


# добавляем пользователей  в групу common при создании
@receiver(post_save, sender=User)
def add_group_on_create(instance, **kwargs):
    common_group = Group.objects.get(name='common')
    common_group.user_set.add(instance)


@receiver(post_save, sender=Comment)
def email_inform(sender, instance, created, **kwargs):
    # Если пользователь написавший комментарий является автором этой же статьи то сразу акцептуем ее
    if instance.user.id == instance.post.author.user.id:
        if created:  # меняем только при создании записи, иначе получится безконечная рекурсия )))
            instance.accepted = True
            instance.save()
    else:
        if not instance.accepted:  # уведомляем автора о создании комментария к его статье
            html_content = render_to_string('email/send_on_comment_add.html', {'comment': instance}, )
            msg = EmailMultiAlternatives(
                subject="Получен отклик к вашей статье",
                from_email='stwski@inbox.ru',
                to=[instance.post.author.user.email])  # емейл автора статьи к которому написан коммент
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        else:  # уведомляем пользователя об акцепте его комментария
            if instance.accepted:
                html_content = render_to_string('email/send_on_comment_accepted.html', {'comment': instance}, )
                msg = EmailMultiAlternatives(
                    subject="Ваш комментарий подтверден",
                    from_email='stwski@inbox.ru',
                    to=[instance.user.email])  # емейл юзера написавшего коммент
                msg.attach_alternative(html_content, "text/html")
                msg.send()

