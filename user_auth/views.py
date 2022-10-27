from django.shortcuts import render
from user_auth.models import CustomUser
from rest_framework import generics
from user_auth.serializers import CustomUserSeriallizer, RoleSerilaizer, UserGroupSerializer


class UserListView(generics.ListAPIView):
    serializer_class = CustomUserSeriallizer
    queryset = CustomUser.objects.all()
    
class RegisterView(generics.CreateAPIView):
    serializer_class = CustomUserSeriallizer
    queryset = CustomUser.objects.all()
    
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUserSeriallizer
    queryset = CustomUser.objects.all()
    


    
