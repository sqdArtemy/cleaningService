from celery import shared_task
from django.core.mail import send_mail
from final_project.settings import settings


@shared_task(bind=True)
def mail_sender_task(self, user_mails, header, text, *args, **kwargs):  # Task which will send notification mails
    print(user_mails)
    for mail in user_mails:
        print(mail)
        send_mail(
            subject=header,
            message=text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=('sqd.artemy@gmail.com',),
            fail_silently=False,
        )
    return 'Done'
