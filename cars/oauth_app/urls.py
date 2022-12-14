from django.contrib.auth.views import LogoutView
from django.urls import path
from .signals import *
from cars.oauth_app.views import UserRegisterView, UserLogInView, UserDeleteView, UserChangePassword, \
    AdminControlView, BanUnbanView
from ..core.emails import activate

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='Register'),
    path('log-in/', UserLogInView.as_view(), name='Log in'),
    path('log-out/', LogoutView.as_view(), name='Log out'),
    path('delete/', UserDeleteView.as_view(), name='Delete user'),
    path('password/change/', UserChangePassword.as_view(), name='Change password'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('admin/panel/', AdminControlView.as_view(), name='admin panel'),
    path('ban/<int:pk>/', BanUnbanView.as_view(), name='profile ban'),
]
