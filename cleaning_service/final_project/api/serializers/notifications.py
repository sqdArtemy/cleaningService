from rest_framework import serializers

from core.models import Notification, Request


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('user', 'header', 'text', 'request', 'seen', 'accepted')

    user = serializers.CharField(source="user.username")

    @staticmethod
    def get_user(notification):
        return notification.user.username
