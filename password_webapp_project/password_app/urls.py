from django.urls import path

from . import views

app_name = 'password_app'
urlpatterns = [
    path('', views.PasswordListView.as_view(), name='list'),
    path('show/<int:pk>/', views.PasswordDetailView.as_view(), name='detail'),
    path('add/', views.PasswordCreateView.as_view(), name='add'),
    path('update/<int:pk>/', views.PasswordUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.PasswordDeleteView.as_view(), name='delete'),
    path('remove_from_shared/<int:pk>/', views.RemoveUserFromSharedPasswordUsers.as_view(), name='remove_from_shared'),
    path('export_csv/', views.PasswordExportToCSV.as_view(), name='export_to_csv'),
]