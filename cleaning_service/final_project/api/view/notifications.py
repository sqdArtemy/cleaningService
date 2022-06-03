from core.models import Notification, User, Request
from api.serializers import NotificationSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def get_user(self, username):
        return User.objects.filter(username=username).first()

    def get_request(self, id):
        return Request.objects.get(id=1)

    def get_queryset(self):
        notifications = Notification.objects.select_related('user', 'request')
        return notifications

    def create(self, request, *args, **kwargs):
        data = request.data

        notification = Notification.objects.create(seen=data['seen'], text=data['text'], header=data['header'],
                                                   user=self.get_user(data["user"]), accept = data['accept'],
                                                   request=self.get_request(data['request']))
        notification.save()
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)
