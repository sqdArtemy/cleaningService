from core.models import Request, User, UserRole, Notification
from core.tasks import mail_sender_task

def notification_maker(request, users, header, text):  # Creating notification object
    user_mails = []
    for user in users:  # Getting user mails
        user_mails.append(user.email)
    # Sending mails to users
    # mail_sender_task.delay(user_mails=user_mails, text=text, header=header)
    for user in users:  # Sending notification to all needed users
        new_notification = Notification.objects.create(
            request=request,
            header=header,
            text=text,
            user=user,
            seen=False,
            accepted=False,
        )


# Receive signals when request created by user and notify all companies
def company_notifier_signal(sender, instance: Request, **kwargs):
    print('signal to company ------')
    # Making data
    companies = User.objects.filter(role__role="Company")
    header = 'New request available, check it out!'
    text = f'New request for cleaning available! \nService: {instance.service.name}\nCustomer details:' \
           f'\n\tName: {instance.customer.name}\n\tEmail: {instance.customer.email}'

    # Process notifications
    notification_maker(request=instance, header=header, text=text, users=companies)
