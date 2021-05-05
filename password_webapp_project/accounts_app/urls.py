from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts_app'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="accounts_app/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('afterLogout/', views.AfterLogoutView.as_view(), name="afterLogout"),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('account_settings/', views.AccountSettingsView.as_view(), name='account_settings'),
    path('account_change_password/', views.AccountChangePasswordView.as_view(), name='account_change_password'),
    path('account_change_email/', views.AccountChangeEmailView.as_view(), name='account_change_email'),
    # path(r'^after_signup/$', views.AfterRegisterPage.as_view(), name="after_signup"),
    #
    # path(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    # path(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    # path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     auth_views.password_reset_confirm, name='password_reset_confirm'),
    # path(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

]
