import sys

import factory
from django.forms.models import model_to_dict
from factory.django import DjangoModelFactory

sys.path.append('..')
from django.core.files.base import ContentFile

from core.models import (Category, Notification, Request, RequestStatus,
                         Review, Service, User, UserRole)


# Factories for service.py ---------------------------------------------------------------------------------------------
class CategoryFactory(DjangoModelFactory):  # Factory creates random categories for services
    class Meta:
        model = Category

    naming = factory.faker.Faker('color')


class ServiceFactory(DjangoModelFactory):  # This factory creates services with random data
    class Meta:
        model = Service

    name = factory.faker.Faker('company')
    category = factory.SubFactory(CategoryFactory)
    cost = factory.faker.Faker('pyint')
    picture = factory.LazyAttribute(  # Faking some picture
            lambda _: ContentFile(
                factory.django.ImageField()._make_data(
                    {'width': 1024, 'height': 768}
                ), 'example.jpg')
            )


# Factories for profiles.py --------------------------------------------------------------------------------------------
class UserRoleFactory(DjangoModelFactory):  # This factory creates sample user roles
    class Meta:
        model = UserRole

    role = factory.Iterator(["Customer", "Company"])


class UsersFactory(DjangoModelFactory):  # This factory creates users with random data
    class Meta:
        model = User

    username = factory.faker.Faker('email')
    name = factory.faker.Faker('first_name')
    email = factory.faker.Faker('email')
    phone = factory.faker.Faker('phone_number')
    country = factory.faker.Faker('country')
    city = factory.faker.Faker('city')
    address_details = factory.faker.Faker('address')
    role = factory.SubFactory(UserRoleFactory)
    password = factory.faker.Faker('password')
    rating = factory.faker.Faker('pyint', min_value=1, max_value=5)
    profile_pic = None

    @factory.post_generation
    def services(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of services were passed in, use them
                self.services.add(*extracted)


# Factories for request.py ---------------------------------------------------------------------------------------------
class RequestStatusFactory(DjangoModelFactory):  # This factory creates random statuses for requests
    class Meta:
        model = RequestStatus

    status = factory.Iterator(["Pending", "Accepted", "Done"])


class RequestFactory(DjangoModelFactory):  # This factory creates requests with random data
    class Meta:
        model = Request

    service = factory.SubFactory(ServiceFactory)
    customer = factory.SubFactory(UsersFactory)
    status = factory.SubFactory(RequestStatusFactory)
    company = factory.SubFactory(UsersFactory)
    country = factory.faker.Faker('country')
    city = factory.faker.Faker('city')
    address_details = factory.faker.Faker('address')
    total_area = factory.faker.Faker('pyint')


# Factories for reviews.py ---------------------------------------------------------------------------------------------
class ReviewFactory(DjangoModelFactory):
    class Meta:
        model = Review

    request = factory.SubFactory(RequestFactory)
    customer = factory.SubFactory(UsersFactory)
    feedback = factory.faker.Faker('text')
    rate = factory.faker.Faker('pyint', min_value=1, max_value=5)
    created_at = factory.faker.Faker('date_time')


# Factories for notifications.py ---------------------------------------------------------------------------------------
class NotificationFactory(DjangoModelFactory):
    class Meta:
        model = Notification

    user = factory.SubFactory(UsersFactory)
    seen = True
    header = factory.faker.Faker('text')
    text = factory.faker.Faker('text')
    request = factory.SubFactory(RequestFactory)
    accepted = False
