from django.apps import AppConfig


class AppointmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointment'


    from .tasks import send_mails
    from .scheduler import appointment_scheduler
    print('started')

    appointment_scheduler.add_job(
        id='send mails',
        func=send_mails,
        trigger='interval',
        seconds=1000,
    )
    appointment_scheduler.start()



