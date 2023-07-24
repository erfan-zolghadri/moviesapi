from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        username = self.validated_data.get("username")
        email = self.validated_data.get("email")
        password = self.validated_data.get("password")
        password2 = self.validated_data.get("password2")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"error": "User with this email already exists"}
            )

        if password != password2:
            raise serializers.ValidationError({"error": "Your passwords do not match"})

        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()

        return user
