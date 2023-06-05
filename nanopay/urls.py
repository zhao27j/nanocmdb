from django.urls import path

from . import views


app_name = 'nanopay'

urlpatterns = [
    path('legal_entity/<int:pk>/update/', views.LegalEntityUpdateView.as_view(), name='legal-entity-update'),
    path('legal_entity/new/', views.LegalEntityCreateView.as_view(), name='legal-entity-new'),
    path('legal_entity/<int:pk>/detail/', views.LegalEntityDetailView.as_view(), name='legalentity-detail'),
    path('legal_entities', views.LegalEntityListView.as_view(), name='legal-entity-list'),
]

urlpatterns += [
    path('', views.ContractListView.as_view(), name='contract-list'),
    path('contract/<int:pk>/detail/', views.ContractDetailView.as_view(), name='contract-detail'),
    path('contract/<int:pk>/detail/scanned_copy/', views.contract_detail_scanned_copy, name='contract-detail-scanned-copy'),
    # path('contract/new/', views.ContractCreateView.as_view(), name='contract-new'),
    path('contract/new/', views.contract_new, name='contract-new'),
]

urlpatterns += {
    path('payment_term/<int:pk>/new/', views.payment_term_new, name='payment-term-new'),

    path('payment_request/<pk>/paper_form/', views.payment_request_paper_form, name='paper-form'),
    path('payment_request/<pk>/approved/', views.payment_request_approved, name='payment-request-approved'),
    path('payment_request/<int:pk>/new/', views.payment_request_new, name='payment-request-new'),
    path('payment_requests', views.PaymentRequestListView.as_view(), name='payment-request-list'),
    # path('payment_requests/<pk>/detail/', views.PaymentRequestDetailView.as_view(), name='payment-request-detail'),
    path('payment_requests/<pk>/detail/invoice_scanned_copy/', views.payment_request_detail_invoice_scanned_copy, name='payment-request-detail-invoice-scanned-copy'),
}