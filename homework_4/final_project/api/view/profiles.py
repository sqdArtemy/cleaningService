from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views.generic import DetailView
from django.http import HttpResponse
import sys
sys.path.append("...")
from core.models.profiles import User


def get_users(request):  # Get all user
    if request.method == "GET":
        users = User.objects.all()
        result = []
        for user in users:
            result.append(user.name)
        return HttpResponse(result)


class UserDetailsView(DetailView):  # Detail view
    model = User
    template_name = "user_detail.html"


class DeleteUserView(DeleteView):  # Deleting user record
    model = User
    success_url = "/"
    template_name = "user_confirm_delete.html"


class UpdateUser(UpdateView):  # Updating user record
    model = User
    success_url = "/"
    fields = ['name', 'email', 'phone']
    template_name = "update.html"


class CreateUserView(CreateView):  # Create new users
    model = User
    fields = ['name', 'email', 'phone', 'role']
    template_name = "create.html"
    success_url = "/"