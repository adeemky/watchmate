from watchlist_app.models import WatchList, StreamPlatform, Review
from . import serializers, pagination, throttling, permissions
from rest_framework import viewsets, generics, filters
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend


# REVIEW
class UserReview(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer
    throttle_classes = [throttling.ReviewListThrottle, AnonRateThrottle]

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)

class ReviewCreate(generics.CreateAPIView):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [throttling.ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You are already reviewed this movie")

        new_rating = serializer.validated_data["rating"]
        WatchList.objects.filter(pk=pk).update(
        avg_rating=((F('avg_rating') * F('number_rating')) + new_rating) / (F('number_rating') + 1),
        number_rating=F('number_rating') + 1
        )
            
        serializer.save(watchlist=watchlist, review_user=review_user)

class ReviewList(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer
    throttle_classes = [throttling.ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'rating']
    
    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'
    

# STREAM
class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]

# WATCHLIST
class WatchListGV(generics.ListCreateAPIView):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListSerializer
    
    permission_classes = [permissions.IsAdminOrReadOnly]
    pagination_class = pagination.WatchListPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'platform__name']


class WatchDetailAV(generics.RetrieveUpdateDestroyAPIView):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]
    