from rest_framework.schemas import ManualSchema
from rest_framework.compat import coreapi, coreschema
from rest_framework.authtoken import views as auth_views
from django.shortcuts import render
from user_auth.models import CustomUser
from rest_framework import generics, status
from user_auth.serializers import CustomUserSeriallizer, RoleSerilaizer, UserGroupSerializer, MyAuthTokenSerializer, LoginSerializer
# from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate



class UserListView(generics.ListAPIView):
    permission_classes = [
        IsAuthenticated
    ]
    serializer_class = CustomUserSeriallizer
    queryset = CustomUser.objects.all()


class RegisterView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = []

    serializer_class = CustomUserSeriallizer
    queryset = CustomUser.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticated
    ]
    serializer_class = CustomUserSeriallizer
    queryset = CustomUser.objects.all()


class LoginView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer
    queryset = CustomUser.objects.all()

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"msg": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
