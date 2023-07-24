from django.urls import path

from .views import (
    MovieList,
    MovieDetail,
    StreamingPlatformList,
    StreamingPlatformDetail,
    ReviewList,
    ReviewCreate,
    ReviewDetail,
)

urlpatterns = [
    path(
        "streaming-platforms/",
        StreamingPlatformList.as_view(),
        name="streaming-platform-list",
    ),
    path(
        "streaming-platforms/<int:pk>/",
        StreamingPlatformDetail.as_view(),
        name="streaming-platform-detail",
    ),
    path("movies/", MovieList.as_view(), name="movie-list"),
    path("movies/<int:pk>/", MovieDetail.as_view(), name="movie-detail"),
    path("movies/<int:pk>/reviews/", ReviewList.as_view(), name="review-list"),
    path("movies/<int:pk>/reviews/new/", ReviewCreate.as_view(), name="review-create"),
    path("movies/reviews/<int:pk>/", ReviewDetail.as_view(), name="review-detail"),
]
