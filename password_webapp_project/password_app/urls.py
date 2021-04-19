from django.urls import path

from . import views

app_name = 'password_app'
urlpatterns = [
    path('', views.PasswordListView.as_view(), name='list'),
    path('show/<int:pk>/', views.PasswordDetailView.as_view(), name='detail'),
    path('add/', views.PasswordDetailView.as_view(), name='add'),
    path('update/<int:pk>/', views.PasswordDetailView.as_view(), name='update'),
    path('delete/<int:pk>/', views.PasswordDetailView.as_view(), name='delete'),
]