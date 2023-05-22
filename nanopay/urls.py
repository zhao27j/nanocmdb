from django.urls import path

from . import views


app_name = 'nanopay'
urlpatterns = [
    path('', views.ContractListView.as_view(), name='contract-list'),
    path('contract/<int:pk>/detail/', views.ContractDetailView.as_view(), name='contract-detail'),
    path('contract/<int:pk>/detail/scanned_copy/', views.contract_detail_scanned_copy, name='contract-detail-scanned-copy'),
    # path('contract/new/', views.ContractCreateView.as_view(), name='contract-new'),
    path('contract/new/', views.new_contract, name='contract-new'),
]

urlpatterns += {
    path('payment_term/<int:pk>/new/', views.new_payment_term, name='payment-term-new'),
    path('payment_request/<int:pk>/new/', views.new_payment_request, name='payment-request-new'),
    path('payment_requests', views.PaymentRequestListView.as_view(), name='payment-request-list'),
    path('payment/<pk>/detail/', views.PaymentRequestDetailView.as_view(), name='payment-request-detail'),
}