from django.urls import path

from . import views

app_name = 'nanobase'

urlpatterns = [
    path('index/', views.index, name='index'),
]

urlpatterns += [
    # path('user/new/', views.UserCreateView.as_view(), name='user-new'),
    path('user/new/', views.user_create, name='user-new'),
    path('user_profile/<int:pk>/update/', views.user_profile_update, name='user-profile-update'),
]


# digital copy
urlpatterns += [
    path('digital_copy/<int:pk>/display/', views.get_digital_copy_display, name='digital-copy-display'),
    path('digital_copy/<int:pk>/delete/', views.get_digital_copy_delete, name='digital-copy-delete'),
    path('digital_copy/<int:pk>/<db_table_name>/add/', views.get_digital_copy_add, name='digital-copy-add'),
]

# json response
urlpatterns += [
    path('json_response/owner_list', views.jsonResponse_owner_list, name='jsonResponse-owner-list'),
]

# temp - data migrations
urlpatterns += [
    # path('temp_data_migration/', views.data_migration_ActivityHistory_to_ChangeHistory, name='temp-data-migration'),
]