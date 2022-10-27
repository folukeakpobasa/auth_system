from django.urls import path
from user_auth import views

urlpatterns = [
    path('user-list', views.UserListView.as_view(), name='user-list'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('user/<int:pk>', views.UserDetailView.as_view(), name='detail'),
]
