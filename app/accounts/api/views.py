from rest_framework import generics
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from .serializers import UserSerializer


class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# @api_view(["POST"])
# def logout_view(request):
#     if request.method == "POST":
#         request.user.auth_token.delete()
#         return Response(status=status.HTTP_200_OK)
