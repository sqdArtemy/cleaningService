"""final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework import routers
import sys
sys.path.append("..")
from api.view.profiles import user_roles_list, users_list, UserDetails, UsersList, UserRolesList, UserRoleDetails, UserViewSet
from api.view.request import request_statuses_list, requests_list,RequestStatusDetails, RequestStatusesList,RequestsList,RequestDetails, RequestViewSet
from api.view.service import categories_list, CategoryCreate,CategoryDetails, services_list,ServicesList, ServiceDetails, CategoryViewSet, ServiceViewSet
from api.view.reviews import reviews_list, ReviewDetails, ReviewsList, ReviewViewSet

router = routers.SimpleRouter()
router.register(r'categories_viewset', CategoryViewSet)
router.register(r'services_viewset', ServiceViewSet)
router.register(r'users_viewset', UserViewSet)
router.register(r'review_viewset', ReviewViewSet)
router.register(r'request_viewset',RequestViewSet)
urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    # User role paths
    path('user_roles_list/', user_roles_list),
    path('<pk>/user_role_details/', UserRoleDetails.as_view()),
    path('generics_user_roles_list', UserRolesList.as_view()),
    # User paths
    path('users_list/', users_list),
    path('<pk>/user_details/', UserDetails.as_view()),
    path('generics_users_list/', UsersList.as_view()),
    # Request status paths
    path('request_statuses_list/', request_statuses_list),
    path('<pk>/request_status_details/', RequestStatusDetails.as_view()),
    path('generics_request_statuses_list/', RequestStatusesList.as_view()),
    # Request paths
    path('requests_list/', requests_list),
    path('<pk>/request_details/', RequestDetails.as_view()),
    path('generics_requests_list/', RequestsList.as_view()),
    # Review paths
    path('reviews_list/', reviews_list),
    path('<pk>/review_details/', ReviewDetails.as_view()),
    path('generics_reviews_list/', ReviewsList.as_view()),
    # Category oaths
    path('categories_list/', categories_list),
    path('<pk>/category_details/', CategoryDetails.as_view()),
    path('generics_category_create/', CategoryCreate.as_view()),
    # Service
    path('services_list/', services_list),
    path('<pk>/service_details/', ServiceDetails.as_view()),
    path('generics_services_list/', ServicesList.as_view()),
]
