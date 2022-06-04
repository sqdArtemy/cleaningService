from django.contrib import admin
from core.models import User, UserRole, Category, Service, Request, RequestStatus, Review, Notification


# Admin registration for profiles.py------------------------------------------------------------------------------------
@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'role')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'role', 'email', 'phone', 'country', 'city', 'address_details')


# Admin registration for service.py-------------------------------------------------------------------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'naming')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')


# Admin registration for request.py-------------------------------------------------------------------------------------
@admin.register(RequestStatus)
class RequestStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'customer', 'total_cost', 'total_area', 'city', 'country')


# Admin registration for reviews.py-------------------------------------------------------------------------------------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('request', 'rate', 'created_at')


# Admin registration for notifications.py-------------------------------------------------------------------------------
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'request', 'seen', 'accepted', 'header')
