from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.core.exceptions import PermissionDenied

from core.models import Notification, Order, Request, User, UserRole, RequestStatus
from core.tasks import mail_sender_task


def notification_maker(request, users, header, text):  # Creating notification object
    user_mails = []
    for user in users:  # Getting user mails
        user_mails.append(user.email)

    # Sending mails to users
    mail_sender_task.delay(user_mails=user_mails, text=text, header=header)
    for user in users:  # Sending notification to all needed users
        Notification.objects.create(
            request=request,
            header=header,
            text=text,
            user=user,
            seen=False,
            accepted=False,
        )


# Receive signals when request created by user and notify all companies
def company_notifier_signal(sender, instance: Request, **kwargs):
    # Filtering companies to match given filters
    companies = User.objects.filter(role__role="Company", rating__gte=int(instance.min_rating_needed),
                                    meter_cost__lte=float(instance.max_meter_cost), country=instance.country,
                                    city=instance.city, services__in=[instance.service])

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
    if instance.accepted == '1':
        if instance.notification.request.status.status == 'Pending':
            # Changing parameters of a request
            instance.request.total_cost = instance.total_cost
            instance.request.company = instance.notification.user
            instance.request.status = RequestStatus.objects.get(status='Accepted')
            instance.request.save()
        else:
            raise PermissionDenied("Request is already processing by another company!")
