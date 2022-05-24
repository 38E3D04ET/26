from django.shortcuts import render, reverse, redirect
from django.template.loader import render_to_string
from django.views import View
from django.core.mail import send_mail, EmailMultiAlternatives, mail_admins
from datetime import datetime

from .models import Appointment



class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # отправляем письмо всем админам по аналогии с send_mail, только здесь получателя указывать не надо
        mail_admins(
            subject=f'{appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
            message=appointment.message,
        )




        # получаем наш html
        #html_content = render_to_string(
        #    'appointment_created.html',
        #    {
        #        'appointment': appointment,
        #    }
        #)

        # отправляем письмо
        #msg = EmailMultiAlternatives(
        #    subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
        #    body=appointment.message,
        #    from_email='ai333i@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
        #    to=['alf.alexy@yandex.ru']  # здесь список получателей. Например, секретарь, сам врач и т. д.
        #)

        #msg.attach_alternative(html_content, "text/html")  # добавляем html

        #msg.send()  # отсылаем

        return redirect('/appointment')



