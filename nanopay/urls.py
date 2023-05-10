from django.urls import path

from . import views


app_name = 'nanopay'
urlpatterns = [
    path('', views.ContractListView.as_view(), name='contract-list'),
    path('contract/<int:pk>/detail/', views.ContractDetailView.as_view(), name='contract-detail'),
    # path('contract/new/', views.ContractCreateView.as_view(), name='contract-new'),
    path('contract/new/', views.new_contract, name='contract-new'),
]