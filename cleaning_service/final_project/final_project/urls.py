from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from rest_framework import permissions
import debug_toolbar
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api.view import UserRoleViewSet, UserViewSet, ReviewViewSet, CategoryViewSet, ServiceViewSet, \
    RequestStatusViewSet, RequestViewSet, NotificationViewSet, OrderViewSet


# Swagger view
schema_view = get_schema_view(
   openapi.Info(
      title="Cleaning service API",
      default_version='v1',
      description="API for cleaning service companies and customers who can create requestes for cleaning their places",
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny, ),
)

urlpatterns = [
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
    # Service paths
    path('services/', ServiceViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('service/<pk>', ServiceViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
    # Notification paths
    path('notifications/', NotificationViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('notification/<pk>', NotificationViewSet.as_view({'get': 'retrieve', 'delete': 'destroy',
                                                       'put': 'partial_update'})),
    # Order paths
    path('orders/', OrderViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('order/<pk>', OrderViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'partial_update'})),
    # JWT auth
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Paths only for development mode
if settings.DEBUG is True:
    urlpatterns += [
        # Debug toolbar
        path('__debug__/', include(debug_toolbar.urls)),
    ]