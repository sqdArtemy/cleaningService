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
import sys
sys.path.append("..")
from api.view import profiles
from api.view.profiles import UserDetailsView, DeleteUserView, UpdateUser, CreateUserView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('function_view/', profiles.get_users),
    path('<pk>/get_detailed_user/', UserDetailsView.as_view()),
    path('<pk>/delete_user/', DeleteUserView.as_view()),
    path('<pk>/update_user', UpdateUser.as_view()),
    path('create_user/', CreateUserView.as_view()),
]
