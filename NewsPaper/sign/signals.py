from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers, mail_admins

from Newspaper import appointment
from Newspaper.sign.models import User
from Newspaper.sign.views import BaseRegisterForm


