import factory
import sys
from django.forms.models import model_to_dict
from factory.django import DjangoModelFactory
sys.path.append('..')
from core.models import User, UserRole, Request, RequestStatus, Service, Category, Review


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
    role = factory.SubFactory(UserRoleFactory)
    password = factory.faker.Faker('password')


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
    company = factory.SubFactory(UsersFactory)


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
    address = factory.faker.Faker('address')
    total_area = factory.faker.Faker('pyint')


# Factories for reviews.py ---------------------------------------------------------------------------------------------
class ReviewFactory(DjangoModelFactory):
    class Meta:
        model = Review

    request = factory.SubFactory(RequestFactory)
    customer = factory.SubFactory(UsersFactory)
    feedback = factory.faker.Faker('text')
    rate = factory.faker.Faker('pyint')
    created_at = factory.faker.Faker('date_time')

# Pattern functions for creating objects
def create_sample_user(dictionary):
    user_role = UserRole.objects.create(id=dictionary.role.id, role=dictionary.role.role)
    user = User.objects.create(
        id=dictionary.id,
        username=dictionary.username,
        name=dictionary.name,
        phone=dictionary.phone,
        role=user_role,
        password=dictionary.password,
    )
    return user

def create_sample_service(dictionary):
    category = Category.objects.create(id=dictionary.category.id, naming=dictionary.category.naming)
    company = dictionary.company
    company.role.save()
    company.save()
    Service.objects.create(
        id=dictionary.id,
        category=category,
        cost=dictionary.cost,
        name=dictionary.name,
        company=company,
    )

def create_sample_request(dictionary, customer):
    dictionary.service.category.save()
    dictionary.service.company.role.save()
    dictionary.service.company.save()
    dictionary.status.save()
    service = Service.objects.create(  # Creating service object
        id=dictionary.service.id,
        cost=dictionary.service.cost,
        name=dictionary.service.name,
        category=dictionary.service.category,
        company=dictionary.service.company,
    )

    my_request = Request.objects.create(  # Creating sample Request object
        id=dictionary.id,
        status=dictionary.status,
        customer=customer,
        service=service,
        total_area=dictionary.total_area,
        address=dictionary.address,
    )
    return my_request