from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts_app'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="accounts_app/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('afterLogout/', views.AfterLogoutView.as_view(), name="afterLogout"),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('password_reset/', views.PasswordResetRequest.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="accounts_app/password_reset_done.html"),
         name='password_reset_done'),
    path('reset_password/<uidb64>/(<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts_app/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts_app/password_reset_complete.html"),
         name='password_reset_complete'),

    path('account_settings/', views.AccountSettingsView.as_view(), name='account_settings'),
    path('account_change_password/', views.AccountChangePasswordView.as_view(), name='account_change_password'),
    path('account_change_email/', views.AccountChangeEmailView.as_view(), name='account_change_email'),

]
