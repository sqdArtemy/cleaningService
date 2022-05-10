from rest_framework import serializers
import sys
sys.path.append("...")
from core.models.reviews import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'request', 'customer', 'feedback', 'rate', 'created_at']