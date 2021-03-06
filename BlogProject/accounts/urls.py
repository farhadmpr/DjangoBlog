from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/<int:user_id>', views.user_profile, name='profile'),
    path('edit_profile/<int:user_id>', views.edit_profile, name='edit_profile'),
    path('mobile_login/', views.mobile_login, name='mobile_login'),
    path('mobile_verify/<str:mobile>/<int:verify_code>/',
         views.mobile_verify, name='mobile_verify'),
    path('follow/', views.follow, name='follow'),
    path('unfollow/', views.unfollow, name='unfollow'),

    path('login2/', auth_views.LoginView.as_view(template_name='accounts/login2.html'), name='login2'),


]
