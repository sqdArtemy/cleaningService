from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.serializers.reviews import ReviewSerializer
from core.models import Request, Review, User


# Views for review
class ReviewViewSet(viewsets.ModelViewSet):  # ViewSet
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ReviewSerializer

    @staticmethod
    def get_customer(username):  # Obtaining user instance
        return User.objects.get(username=username)

    @staticmethod
    def get_request(id_):  # Obtaining request instance
        return Request.objects.get(id=id_)

    def get_queryset(self):
        categories = Review.objects.select_related('customer', 'request')
        return categories

    def destroy(self, request, pk, *args, **kwargs):
        # getting needed data
        review = get_object_or_404(self.get_queryset(), pk=pk)
        company = review.request.company
        previous_rating = float(company.rating)
        previous_users_rated = int(company.users_rated)
        rating_to_delete = float(review.rate)

        # Changing user`s rating because it is deleted
        company.users_rated -= 1
        company.rating = (previous_rating * previous_users_rated - rating_to_delete) / (previous_users_rated - 1)
        company.save()

        return super().destroy(request, pk, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data

        new_review = Review.objects.create(request=self.get_request(data["request"]), feedback=data['feedback'],
                                           customer=self.get_customer(data["customer"]), rate=data['rate'])
        new_review.save()

        # Changing overall rating of a company
        company = new_review.request.company
        if company is not None:
            if company.rating <= 0:
                company.rating = new_review.rate
            else:
                company.rating = (float(company.rating) * int(company.users_rated) + float(new_review.rate)) / (int(
                    company.users_rated) + 1)

        # Increase counter of a users who have rated the company
        company.users_rated += 1
        company.save()

        serializer = ReviewSerializer(new_review)
        return Response(serializer.data)

    def update(self, request, pk):
        data = request.data
        review_object = self.get_queryset()
        review = get_object_or_404(review_object, pk=pk)
        unchanged_review = get_object_or_404(review_object, pk=pk)

        # Updating current requests
        review.request = review.request
        review.customer = review.customer
        review.feedback = data['feedback']
        review.rate = data['rate']
        review.save()

        # Updating rating of a company
        company = review.request.company
        if company is not None:
            # Getting previous rating data
            old_rating = float(company.rating)
            users_rated = int(company.users_rated)

            print(old_rating)

            # Performing changes
            company.rating = ((old_rating * users_rated - float(unchanged_review.rate)) +
                              float(review.rate)) / users_rated

            # Saving result
            company.save()

        serializer = ReviewSerializer(review)
        return Response(serializer.data)
