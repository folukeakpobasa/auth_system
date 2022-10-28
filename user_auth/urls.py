from django.urls import path
from user_auth import views

urlpatterns = [
    path('users', views.UserListView.as_view(), name='users'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('users/<int:pk>', views.UserDetailView.as_view(), name='detail'),
    path('login/', views.LoginView.as_view(), name="login")
]
