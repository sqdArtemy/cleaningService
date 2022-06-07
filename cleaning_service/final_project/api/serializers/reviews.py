from rest_framework import serializers

from core.models.reviews import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['request', 'customer', 'feedback', 'rate', 'created_at']

    customer = serializers.CharField(source='customer.username')
    request = serializers.SerializerMethodField()

    @staticmethod
    def get_customer(review):
        return review.customer.username

    @staticmethod
    def get_request(review):
        return review.request.id
