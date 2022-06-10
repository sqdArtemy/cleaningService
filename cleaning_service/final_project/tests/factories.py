import factory
from django.core.files.base import ContentFile
from factory.django import DjangoModelFactory


from core.models import (Category, Notification, Request, RequestStatus, Review, Service, User, UserRole, Order)

fake_data = factory.faker.Faker  # Just for better comprehension


# Factories for service.py ---------------------------------------------------------------------------------------------
class CategoryFactory(DjangoModelFactory):  # Factory creates random categories for services
    class Meta:
        model = Category

    naming = fake_data('color')


class ServiceFactory(DjangoModelFactory):  # This factory creates services with random data
    class Meta:
        model = Service

    name = fake_data('email')
    category = factory.SubFactory(CategoryFactory)
    description = fake_data('text')
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

    username = fake_data('email')
    name = fake_data('first_name')
    email = fake_data('email')
    phone = fake_data('phone_number')
    country = fake_data('country')
    city = fake_data('city')
    address_details = fake_data('address')
    role = factory.SubFactory(UserRoleFactory)
    password = fake_data('password')
    rating = fake_data('pyint', min_value=1, max_value=5)
    meter_cost = fake_data('pyint')
    users_rated = fake_data('pyint')
    picture = None

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

    status = factory.Iterator(["Pending"])


class RequestFactory(DjangoModelFactory):  # This factory creates requests with random data
    class Meta:
        model = Request

    service = factory.SubFactory(ServiceFactory)
    customer = factory.SubFactory(UsersFactory)
    status = factory.SubFactory(RequestStatusFactory)
    company = factory.SubFactory(UsersFactory)
    country = fake_data('country')
    city = fake_data('city')
    address_details = fake_data('address')
    total_area = fake_data('pyint')
    min_rating_needed = fake_data('pyint', min_value=0, max_value=5)
    max_meter_cost = fake_data('pyint')


# Factories for reviews.py ---------------------------------------------------------------------------------------------
class ReviewFactory(DjangoModelFactory):
    class Meta:
        model = Review

    request = factory.SubFactory(RequestFactory)
    customer = factory.SubFactory(UsersFactory)
    feedback = fake_data('text')
    rate = fake_data('pyint', min_value=1, max_value=5)


# Factories for notifications.py ---------------------------------------------------------------------------------------
class NotificationFactory(DjangoModelFactory):
    class Meta:
        model = Notification

    user = factory.SubFactory(UsersFactory)
    seen = True
    header = fake_data('text')
    text = fake_data('text')
    request = factory.SubFactory(RequestFactory)
    accepted = False


# Factories for order.py -----------------------------------------------------------------------------------------------
class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    notification = factory.SubFactory(NotificationFactory)
    accepted = False
