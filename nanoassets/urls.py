from django.urls import path

from . import views


app_name = 'nanoassets'
urlpatterns = [
    # path('', views.index, name='index'),
]

# Assets Instance
urlpatterns += [
    path('instance_bulk_upd/', views.InstanceBulkUpd, name='instance-bulk-upd'),
    path('instance_search_results/', views.InstanceSearchResultsListView.as_view(), name='instance-search-results'),
]

# Scrapping
urlpatterns += [
    path('instance_scrapping_request_list/', views.InstanceScrappingRequestListView.as_view(), name='instance-scrapping-request-list'),
    path('instance_scrapping_request_detail/<pk>/', views.InstanceScrappingRequestDetailView.as_view(), name='instance-scrapping-request-detail'),
    path('instance_scrapping_request_detail/<pk>/approved/', views.InstanceScrappingRequestApproved, name='instance-scrapping-request-approved'),
]

urlpatterns += [
    path('', views.InstanceByUserListView.as_view(), name='my-instance-list'),
    path('supported_instances/', views.InstanceByTechListView.as_view(), name='supported-instance-list'),
    path('instance/<pk>/detail/', views.InstanceDetailView.as_view(), name='instance-detail'),
    path('instance/<pk>/owner_upd/', views.InstanceOwnerUpdate.as_view(), name='instance-owner-upd'),
    path('instance/<pk>/in_repair/', views.InstanceInRepair, name='instance-in-repair'),
]