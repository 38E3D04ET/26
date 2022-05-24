from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from celery.schedules import crontab
from django.core.mail import send_mail


# таска для отправки писем подписчикам при создании новой
@shared_task
def send_mail_for_sub_once(sub_username, sub_useremail, html_content):
    print('Таска_одно_письмо - старт')
    msg = EmailMultiAlternatives(
        subject=f'Здравствуй, {sub_username}. Новая статья в вашем разделе!',
        from_email='ai333i@yandex.ru',
        to=[sub_useremail]
    )

    msg.attach_alternative(html_content, 'text/html')

    # для удобства вывода инфы в консоль
    print()
    print(html_content)
    print()

    # код ниже временно заблокирован, чтоб в процессе отладки не производилась реальная рассылка писем
    msg.send()
    print('Таска_одно_письмо - конец')
