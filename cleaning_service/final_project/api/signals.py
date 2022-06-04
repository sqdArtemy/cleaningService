from core.models import Request, User, UserRole, Notification
from core.tasks import mail_sender_task
from django.db.models.signals import post_save
from django.dispatch import receiver

def notification_maker(request, users, header, text):  # Creating notification object
    user_mails = []
    for user in users:  # Getting user mails
        user_mails.append(user.email)
    print('HERE ARE MAILS')
    print(user_mails)
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
    # Making data
    companies = User.objects.filter(role__role="Company")
    header = 'New request available, check it out!'
    text = f'New request for cleaning available! \nService: {instance.service.name}\nCustomer details:' \
           f'\n\tName: {instance.customer.name}\n\tEmail: {instance.customer.email}'

    # Process notifications
    notification_maker(request=instance, header=header, text=text, users=companies)


# Receive signals when company accepts offer from its notification:
@receiver(post_save, sender=Notification)
def customer_notifier_signal(sender, instance: Notification, **kwargs):
    if instance.accepted is True and instance.user.role.role == 'Company':
        print('signal to customer-------')
        # Making data
        user = (instance.request.customer,)
        header = f'New response to your request: {instance.request.id} !'
        text = f'The company {instance.user} has proposer offer to your response, check it out!'

        # Process notifications
        notification_maker(request=instance.request, header=header, text=text, users=user)