from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import NotificationSerializer
from core.models import Notification, Request, User
from core.utility.filters import NotificationFilter


class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NotificationFilter

    @staticmethod
    def get_user(username):
        return User.objects.filter(username=username).first()

    @staticmethod
    def get_request(id_):
        return Request.objects.get(id=id_)

    def get_queryset(self):
        notifications = Notification.objects.select_related('user', 'request')
        return notifications

    def retrieve(self, request, pk, *args, **kwargs):
        # If notification is called by id from user-side -> make status seen: True
        request_object = Notification.objects.select_related('user', 'request')
        notification = get_object_or_404(request_object, pk=pk)
        notification.seen = True
        notification.save()
        serializer = self.serializer_class(notification)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data

        notification = Notification.objects.create(seen=data['seen'], text=data['text'], header=data['header'],
                                                   user=self.get_user(data["user"]), accepted=data['accepted'],
                                                   request=self.get_request(data['request']))
        notification.save()
        serializer = self.serializer_class(notification)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        notification = self.get_object()
        data = request.data
        notification.accepted = data['accepted']
        notification.save()
        serializer = NotificationSerializer(notification, partial=True)
        return Response(serializer.data)
