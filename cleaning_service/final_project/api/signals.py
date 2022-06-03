from core.models import Request, User, UserRole, Notification

def notification_maker(request, users, header, text):  # Creating notification object
    for user in users:  # Sending notification to all needed users
        new_notification = Notification.objects.create(
            request=request,
            header=header,
            text=text,
            user=user,
            seen=False,
        )


# Receive signals when request created by user and notify all companies
def company_notifier_signal(sender, instance: Request, **kwargs):
    print('signal to company ------')
    # Making data
    role = UserRole.objects.get(role='Company')
    companies = User.objects.filter(role=role)
    header = 'New request available, check it out!'
    text = ' '.join(('New request available!', 'Service:', instance.service.name,
                    "Customer:", instance.customer.name))

    # Process notifications
    notification_maker(request=instance, header=header, text=text, users=companies)
