from rest_framework import viewsets
from rest_framework.response import Response
from api.serializers.reviews import ReviewSerializer
from core.models.reviews import Review, User, Request
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404


# Views for review
class ReviewViewSet(viewsets.ModelViewSet):  # ViewSet
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ReviewSerializer

    def get_user(self, email):  # Obtaining user instance
        return User.objects.filter(email=email).first()

    def get_request(self, id):  # Obtaining request instance
        return Request.objects.filter(id=id).first()

    def get_queryset(self):
        categories = Review.objects.all()
        return categories

    def create(self, request, *args, **kwargs):
        data = request.data

        new_review = Review.objects.create(request=self.get_request(data["request"]), customer=self.user(data["customer"]),
                                           feedback=data['feedback'], rate=data['rate'], created_at=data['created_at'])
        new_review.save()
        serializer = ReviewSerializer(new_review)
        return Response(serializer.data)

    def list(self, request: Review, *args, **kwargs) -> Response:
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def update(self, request, pk):
        data = request.data
        review_object = Review.objects.all()
        review = get_object_or_404(review_object, pk=pk)

        review.request = self.get_request(data["request"])
        review.customer = self.get_user(data['customer'])
        review.feedback = data['feedback']
        review.rate = data['rate']
        review.created_at = data['created_at']
        review.save()

        serializer = ReviewSerializer(review)
        return Response(serializer.data)

