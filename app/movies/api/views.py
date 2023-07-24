from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import MovieSerializer, StreamingPlatformSerializer, ReviewSerializer
from .permissions import IsAdminUserOrReadOnly, IsReviewUserOrReadOnly
from .pagination import MoviePageNumberPagination
from ..models import Movie, StreamingPlatform, Review


class StreamingPlatformList(generics.ListCreateAPIView):
    queryset = StreamingPlatform.objects.all()
    serializer_class = StreamingPlatformSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class StreamingPlatformDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = StreamingPlatform.objects.all()
    serializer_class = StreamingPlatformSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class MovieList(generics.ListCreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["reviews_average", "streaming_platform__name"]
    search_fields = ["title"]
    ordering_fields = ["reviews_average"]
    pagination_class = MoviePageNumberPagination

    def get_queryset(self):
        return Movie.objects.filter(is_active=True)


class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Review.objects.filter(movie=pk, is_active=True)


class ReviewCreate(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user

        pk = self.kwargs.get("pk")
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if Review.objects.filter(user=user, movie=movie).exists():
            raise ValidationError("You have already added a review")

        rating = serializer.validated_data.get("rating")
        if movie.reviews_count == 0:
            movie.reviews_average = rating
        else:
            movie.reviews_average = (movie.reviews_average + rating) / 2
        movie.reviews_count += 1
        movie.save()

        serializer.save(user=user, movie=movie)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
