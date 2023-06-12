from django.urls import path

from . import views

app_name = 'nanobase'

urlpatterns = [
    path('user/new/', views.UserCreateView.as_view(), name='user-new'),
    path('user_profile/<int:pk>/update/', views.user_profile_update, name='user-profile-update'),
]

# temp - data migrations
urlpatterns += [
    path('temp_data_migration/', views.data_migration_Hostname, name='data-migration'),
]