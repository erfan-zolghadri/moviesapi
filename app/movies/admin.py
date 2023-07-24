from django.contrib import admin
from .models import Movie, StreamingPlatform, Review


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "reviews_count",
        "reviews_average",
        "streaming_platform",
        "is_active",
    ]


admin.site.register(StreamingPlatform)
admin.site.register(Review)
