from rest_framework import serializers
from core.models.reviews import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['request', 'customer', 'feedback', 'rate', 'created_at']

    customer = serializers.SerializerMethodField()
    request = serializers.SerializerMethodField()

    def get_customer(self, review):
        return review.customer.name
    def get_request(self, review):
        return review.request.id