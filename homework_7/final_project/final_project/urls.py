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
from django.urls import path, include
from rest_framework import routers
from api.view import UserDetails, UserRolesList, UserRoleDetails, UserViewSet, ReviewDetails, ReviewViewSet,\
    CategoryDetails, ServiceDetails, CategoryViewSet, ServiceViewSet, RequestStatusDetails, RequestStatusesList, RequestDetails, RequestViewSet


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
    path('user_role/<pk>', UserRoleDetails.as_view()),
    path('user_roles', UserRolesList.as_view()),
    # User paths
    path('users/', UserViewSet.as_view({'get': 'list'})),
    path('user/<pk>', UserDetails.as_view()),
    # Request status paths
    path('request_status/<pk>', RequestStatusDetails.as_view()),
    path('generics_request_statuses_list/', RequestStatusesList.as_view()),
    # Request paths
    path('requests/', RequestViewSet.as_view({'get': 'list'})),
    path('request/<pk>', RequestDetails.as_view()),
    # Review paths
    path('review/<pk>', ReviewDetails.as_view()),
    path('reviews/', ReviewViewSet.as_view({'get': 'list'})),
    # Category oaths
    path('categories/', CategoryViewSet.as_view({'get': 'list'})),
    path('category/<pk>', CategoryDetails.as_view()),
    # Service
    path('services/', ServiceViewSet.as_view({'get': 'list'})),
    path('service/<pk>', ServiceDetails.as_view()),
    #JWT auth
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

]
