from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view
from rest_framework import routers
import debug_toolbar
from api.view import UserRoleViewSet, UserViewSet, ReviewViewSet, CategoryViewSet, ServiceViewSet, RequestStatusViewSet, RequestViewSet


# Routers for ViewSets
router = routers.SimpleRouter()
router.register(r'categories_viewset', CategoryViewSet, basename='Category')
router.register(r'services_viewset', ServiceViewSet, basename='Service')
router.register(r'users_viewset', UserViewSet, basename='User')
router.register(r'review_viewset', ReviewViewSet, basename='Review')
router.register(r'request_viewset',RequestViewSet, basename='Request')
router.register(r'user_role_viewset', UserRoleViewSet, basename='UserRole')
router.register(r'request_status_viewset',RequestStatusViewSet, basename='RequestStatus')
urlpatterns = router.urls

# Swagger view
schema_view = get_swagger_view(title='Cleaning Service API')

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
    # JWT auth
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # Swagger
    path('swagger/', schema_view),
]

# Paths only for development mode
if settings.DEBUG is True:
    urlpatterns += [
        # Debug toolbar
        path('__debug__/', include(debug_toolbar.urls)),
    ]