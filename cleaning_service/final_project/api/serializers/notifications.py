from rest_framework import serializers

from core.models import Notification, Request


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('user', 'header', 'text', 'request', 'seen', 'accepted')

    user = serializers.SerializerMethodField()
    request = serializers.SerializerMethodField()

    def get_user(self, notification):
        return notification.user.username

    def get_request(self, notification):
        return notification.request.id