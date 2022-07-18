from django.contrib.auth import get_user_model

from rest_framework import generics

from users.serializers import RegisterUserSerializer

# Create your views here.


class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterUserSerializer
