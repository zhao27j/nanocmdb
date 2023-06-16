from django.urls import path

from . import views

app_name = 'nanobase'

urlpatterns = [
    # path('user/new/', views.UserCreateView.as_view(), name='user-new'),
    path('user/new/', views.user_create, name='user-new'),
    path('user_profile/<int:pk>/update/', views.user_profile_update, name='user-profile-update'),
    path('digital_copy/<int:pk>/display/', views.get_digital_copy_display, name='digital-copy-display'),
]

# temp - data migrations

urlpatterns += [
    # path('temp_data_migration/', views.data_migration_ActivityHistory_to_ChangeHistory, name='temp-data-migration'),
]