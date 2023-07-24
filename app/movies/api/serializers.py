from rest_framework import serializers
from ..models import Movie, StreamingPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    movie = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"


class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    reviews_count = serializers.IntegerField(read_only=True)
    reviews_average = serializers.FloatField(read_only=True)
    streaming_platform = serializers.StringRelatedField()

    class Meta:
        model = Movie
        fields = "__all__"


class StreamingPlatformSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = StreamingPlatform
        fields = "__all__"
