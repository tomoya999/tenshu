from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views

urlpatterns = [
    path('', include('page.urls')),
    path('tenshu/admin/', admin.site.urls),
    path('admin/', include('admin_honeypot.urls')),
    path('', include('register.urls')),
    path('password_reset/', views.PasswordResetView.as_view(), name='admin_password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
