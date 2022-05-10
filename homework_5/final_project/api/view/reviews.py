import sys
from rest_framework.decorators import api_view
from rest_framework import status, generics, mixins
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.reviews import ReviewSerializer
sys.path.append(".")
from core.models.reviews import Review


# Views for review
@api_view(['GET'])
def reviews_list(request, format=None):  # Function based view
    if request.method == 'GET':
        review = Review.objects.all()
        serializer = ReviewSerializer(review, many=True)
        return Response(serializer.data)


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

