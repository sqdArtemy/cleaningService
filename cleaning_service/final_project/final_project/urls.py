from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.view import UserRoleViewSet, UserViewSet, ReviewViewSet, CategoryViewSet, ServiceViewSet, RequestStatusViewSet, RequestViewSet


router = routers.SimpleRouter()
router.register(r'categories_viewset', CategoryViewSet)
router.register(r'services_viewset', ServiceViewSet)
router.register(r'users_viewset', UserViewSet)
router.register(r'review_viewset', ReviewViewSet)
router.register(r'request_viewset',RequestViewSet)
router.register(r'user_role_viewset', UserRoleViewSet)
router.register(r'request_status_viewset',RequestStatusViewSet)
urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    # User role paths
    path('user_roles/', UserRoleViewSet.as_view({'get': 'list'})),
    path('user_role/<pk>', UserRoleViewSet.as_view({'get': 'retrieve'})),
    # User paths
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('user/<pk>', UserViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
    # Request status paths
    path('request_statuses/', RequestStatusViewSet.as_view({'get': 'list'})),
    path('request_status/<pk>', RequestStatusViewSet.as_view({'get': 'retrieve'})),
    # Request paths
    path('requests/', RequestViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('request/<pk>', RequestViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
    # Review paths
    path('reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('review/<pk>', ReviewViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
    # Category paths
    path('categories/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('category/<pk>', CategoryViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
    # Service
    path('services/', ServiceViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('service/<pk>', ServiceViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
    #JWT auth
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

]
