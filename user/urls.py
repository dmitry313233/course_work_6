from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from user.apps import UserConfig
from user.views import RegisterView, verify, switch_status_user, UserListView, UserCreateView

app_name = UserConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verification/<str:cod>/', verify, name='verification'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('switch_status_user/<int:pk>/', switch_status_user, name='switch_status_user'),
    path('profile/', UserCreateView.as_view(), name='profile'),
]
