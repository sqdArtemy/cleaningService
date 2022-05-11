import sys
from rest_framework import status, generics, viewsets
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers.reviews import ReviewSerializer
sys.path.append(".")
from core.models.reviews import Review


# Views for review
class ReviewsList(generics.ListCreateAPIView):  # Generics views
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = []


class ReviewDetails(APIView):  # APIView
    def get_review(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_review(pk)
        serializer = ReviewSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        review = self.get_review(pk)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_review(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(viewsets.ModelViewSet):  # ViewSet
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def get_queryset(self):
        categories = Review.objects.all()
        return categories

    def create(self, request, *args, **kwargs):
        data = request.data

        new_review = Review.objects.create(request=data["request"], customer=data['customer'],
                                           feedback=data['feedback'], rate=data['rate'], created_at=data['created_at'])
        new_review.save()
        serializer = ReviewSerializer(new_review)
        return Response(serializer.data)

    def list(self, request: Review, *args, **kwargs) -> Response:
        serializer = self.get_serializer(self.get_queryset())
        return Response(serializer.data)

    def update(self, request, pk):
        data = request.data

        review = self.get_object(pk)
        review.request = data["customer"]
        review.customer = data['customer']
        review.feedback = data['feedback']
        review.rate = data['rate']
        review.created_at = data['created_at']
        review.save()

        serializer = ReviewSerializer(review)
        return Response(serializer.data)

