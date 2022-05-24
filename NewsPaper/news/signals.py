from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import m2m_changed, post_save
from django.db.models.signals import post_save
from django.dispatch import receiver
from .views import send_mail_for_sub

from django.template.loader import render_to_string

from NewsPaper.news.models import Post, Category


@receiver(m2m_changed, sender=Post)
def notify_users_news(sender, instance, action, **kwargs):
    full_url = ''.join(['http://', get_current_site(None).domain, ':8000'])
    if action == 'news.add_post':
        list_of_subscribers = []
        print('11111')
        for c in instance.category.all():
            print('222222')
            print('c')
            print('instance.category.all()')
            for usr in c.subscribers.all():
                print('333333')
                print('c.subscribers.all()')
                list_of_subscribers.append(usr)
        for usr in list_of_subscribers:
            print('4444444')
            html_content = render_to_string(
                'mail.html',
                {
                    'post': instance,
                    'usr': usr,
                    'full_url': full_url,
                }
            )

            msg = EmailMultiAlternatives(
                subject=instance.title,
                body=f'Hey there! New post in  your favourite category!'+instance.text,
                from_email='ai333i@yandex.ru',
                to=[alf.alexy@yandex.ru]#to=[f'{usr.email}'],
            )
            msg.attach_alternative(html_content, "text/html")

            msg.send()


#@receiver(m2m_changed, sender=Post.category.throught)
#def send_email_to_subs(sender, instance, action, **kwargs):

#    if action == 'post_add':
#        list_of_subs = []
#        for category in instance.post_category.all():
#            for sub in category.subscriber.all():
#                if sub not in list_of_subs:
#                    list_of_subs.append(sub)
#
#        for user in list_of_subs:
#            send_mail(
#                subject=f'New post in {instance.post_category}!',
#                message=f'{instance.title}...',
#                from_email='ai333i@yandex.ru',
#                recipient_list=['alf.alexy@yandex.ru']
#            )


#@receiver(m2m_changed, sender=Category)
#def notify_users_news(sender, instance, action, **kwargs):
#    full_url = ''.join(['http://', get_current_site(None).domain, ':8000'])
#    if action == 'post_add':
#        list_of_subscribers = []
#        print('11111')
#        for c in instance.category.all():
#            print('222222')
#            print('c')
#            print('instance.postCategory.all()')
#            for usr in c.subscribers.all():
#                print('333333')
#               print('c.subscribers.all()')
#                list_of_subscribers.append(usr)
#        for usr in list_of_subscribers:
#            print('4444444')
            #html_content = render_to_string(
            #    'email/subs_email.html',
            #    {
            #        'post': instance,
            #        'usr': usr,
            #        'full_url': full_url,
            #    }
            #)

#            msg = EmailMultiAlternatives(
 #                subject=instance.title,
#                body=f'Hey there! New post in  your favourite category!'+instance.text,
#                from_email='ai333i@yandex.ru',
#                to=[f'alf.alexy@yandex.ru'],
#                #to=[f'{usr.email}'],
#            )
#            msg.attach_alternative(html_content, "text/html")
#
#            msg.send()

