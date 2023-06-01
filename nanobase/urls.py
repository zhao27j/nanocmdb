from django.urls import path

from . import views

app_name = 'nanobase'

urlpatterns = [
    path('profile/', views.UserProfile, name='user-profile'),
]
