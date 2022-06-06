from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Notification, Order, Request, User, UserRole, RequestStatus
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
    if instance.accepted == '1' and instance.user.role.role == 'Company':
        # Making data
        user = (instance.request.customer,)
        header = f'New response to your request: {instance.request.id} !'
        text = f'The company {instance.user} has proposed order to your response, check it out!'

        # Creates order
        Order.objects.create(accepted=False, notification=instance)

        # Process notifications
        notification_maker(request=instance.request, header=header, text=text, users=user)


# Receives signal from order and make changes in a request
@receiver(post_save, sender=Order)
def request_changer(sender, instance: Order, **kwargs):
    if instance.accepted == '1' and instance.notification.request.status.status == 'Pending':
        # Changing parameters of a request
        instance.request.total_cost = instance.total_cost
        instance.request.company = instance.notification.user
        instance.request.status = RequestStatus.objects.get(status='Accepted')
        instance.request.save()
    else:
        raise "Request is already processing by another company!"
