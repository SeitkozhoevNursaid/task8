from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_activation_code(user, code):
    subject = 'Уведомление с http://django'
    message = f'Привет, для подтверждения пожалуйста перейди по ссылке http://127.0.0.1:8000/email-verify/{code}/'
    from_email = 'nursaid.seitkozhoev@mail.ru'
    recipient_list = [user]
    send_mail(subject, message, from_email, recipient_list)


@shared_task
def send_forgot_password(user, code): 
    subject = 'Здравствуйте'
    message =  f'для сброса пароля пожалуйста перейдите по ссылке, http://127.0.0.1:8000/confirm-forgot-password/{code}/'
    from_email = 'nursaid.seitkozhoev@mail.ru'
    recipient_list = [user]
    send_mail(subject, message, from_email, recipient_list)


@shared_task
def send_reset_password(user, new_password):
    subject = 'Здравствуйте'          
    message = f'Мы сбросили ваш пароль, ваш новый пароль "{new_password}", с уважением Администрация)'
    from_email = 'nursaid.seitkozhoev@mail.ru'
    recipient_list = [user]
    send_mail(subject, message, from_email, recipient_list)
