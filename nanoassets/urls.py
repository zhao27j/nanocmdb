from django.urls import path

from . import views, views_api


app_name = 'nanoassets'

urlpatterns = [
    # path('', views.index, name='index'),
]

# Scrapping
urlpatterns += [
    path('instance_scrapping_request_list/', views.InstanceScrappingRequestListView.as_view(), name='instance-scrapping-request-list'),
    path('instance_scrapping_request_detail/<pk>/', views.InstanceScrappingRequestDetailView.as_view(), name='instance-scrapping-request-detail'),
    path('instance_scrapping_request_detail/<pk>/approved/', views.InstanceScrappingRequestApproved, name='instance-scrapping-request-approved'),
]

# Assets Instance
urlpatterns += [
    path('instance_bulk_upd/', views.InstanceBulkUpd, name='instance-bulk-upd'),
    path('instance_search_results/', views.InstanceSearchResultsListView.as_view(), name='instance-search-results'),
]

urlpatterns += [
    path('', views.InstanceByUserListView.as_view(), name='my-instance-list'),
    path('instances_supported/', views.InstanceByTechListView.as_view(), name='supported-instance-list'),
    path('instance/<pk>/detail/', views.InstanceDetailView.as_view(), name='instance-detail'),
    path('instance/new/', views.InstanceNew, name='instance-new'),

    path('instance/<pk>/owner_upd/', views.InstanceOwnerUpdate, name='instance-owner-upd'),
    path('instance/<pk>/hostname_upd/', views.InstanceHostnameUpdate, name='instance-hostname-upd'),
    path('instance/<pk>/model_type_upd/', views.InstanceModelTypeUpdate, name='instance-model-type-upd'),
    path('instance/<pk>/subcategory_upd/', views.InstanceSubcategoryUpdate, name='instance-subcategory-upd'),
    
    path('instance/<pk>/in_repair/', views.InstanceInRepair, name='instance-in-repair'),
]

# Assets Instance - JSON api
urlpatterns += [
    path('json_response/branchSite_lst/', views_api.jsonResponse_branchSite_lst, name='jsonResponse-branchSite-lst'),
    path('instance/branchSite_transferring_to/', views_api.branchSite_transferring_to, name='instance-branchSite-transferring-to'),

    path('json_response/contract_lst/', views_api.jsonResponse_contract_lst, name='jsonResponse-contract-lst'),
    path('instance/contract_associating_with/', views_api.contract_associating_with, name='instance-contract-associating-with'),
]