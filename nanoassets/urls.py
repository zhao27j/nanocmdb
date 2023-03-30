from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
]

urlpatterns += [
    path('instance_scrapping_request/', views.InstanceScrappingRequest, name='instance-scrapping-request'),
    path('instance_scrapping_request_list/', views.InstanceScrappingRequestListView.as_view(), name='instance-scrapping-request-list')
]

urlpatterns += [
    path('instance_search_results/', views.InstanceSearchResultsListView.as_view(),
         name='instance-search-results'),
]

urlpatterns += [
    path('instances/', views.InstanceListView.as_view(), name='instance-list'),
    path('myinstances/', views.InstanceByUserListView.as_view(),
         name='my-instance-list'),
    path('instance/<pk>/', views.InstanceDetailView.as_view(),
         name='instance-detail'),
    path('instance/new', views.InstanceCreate.as_view(), name='instance-new'),
    path('instance/<pk>/statusupdate/',
         views.InstanceStatusUpdate.as_view(), name='instance-status-upd'),
    path('instance/<pk>/modeltypeupdate/',
         views.InstanceModelTypeUpdate.as_view(), name='instance-modeltype-upd'),
]

urlpatterns += [
    path('modeltypes/', views.ModelTypeListView.as_view(), name='modeltype-list'),
    path('modeltype/<int:pk>/', views.ModelTypeDetailView.as_view(),
         name='modeltype-detail'),
    path('modeltype/new/', views.ModelTypeCreate.as_view(), name='modeltype-new'),
    path('modeltype/<int:pk>/update',
         views.ModelTypeUpdate.as_view(), name='modeltype-upd'),
    path('modeltype/<int:pk>/delete',
         views.ModelTypeDelete.as_view(), name='modeltype-del'),
]
