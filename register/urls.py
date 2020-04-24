from django.urls import path
from . import views
from .forms import LoginForm

app_name = 'register'

urlpatterns = [
    path('login/lock', views.LoginLockView.as_view(), name='loginlock'),
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/done/', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    path('login/', views.LoginView.as_view(form_class=LoginForm), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('top/<pk>/', views.UserTop.as_view(), name='usertop'),
    path('password_change', views.PasswordChange.as_view(), name='password_change'),
    path('account/', views.account_redirect, name='account-redirect'),
    path('email/change/', views.EmailChange.as_view(), name='email_change'),
    path('email/change/done/', views.EmailChangeDone.as_view(), name='email_change_done'),
    path('email/change/complete/<str:token>', views.EmailChangeComplete.as_view(),name='email_change_complete'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
]
