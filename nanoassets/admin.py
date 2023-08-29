from django.contrib import admin

from import_export.admin import ImportExportModelAdmin, ImportExportMixin

from .resources import InstanceResource
from .models import Instance, ModelType, Manufacturer, branchSite, disposalRequest, ScrapRequest

# Register your models here.


@admin.register(branchSite)
class branchSiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_onSiteTech', 'city', 'addr',]
    autocomplete_fields = ['country',]


@admin.register(ScrapRequest)
class ScrapRequestAdmin(admin.ModelAdmin):
    list_display = ['case_id', 'status', 'requested_by', 'requested_on', 'approved_by', 'approved_on',]


@admin.register(disposalRequest)
class disposalRequestAdmin(admin.ModelAdmin):
    list_display = ['case_id', 'type', 'status', 'requested_by', 'requested_on', 'approved_by', 'approved_on',]


@admin.register(Instance)
class InstanceAdmin(ImportExportModelAdmin):
    resource_classes = [InstanceResource]

    list_display = ['serial_number', 'model_type', 'hostname',
                    'status', 'eol_date', 'owner', 'branchSite']
    list_filter = ['model_type', 'status', 'branchSite']
    search_fields = ['serial_number', 'model_type__name','status', 'owner__username', 'eol_date']

@admin.register(ModelType)
class ModelTypeAdmin(admin.ModelAdmin):
    list_display = ['sub_category', 'manufacturer', 'name', ]

"""
@admin.register(ActivityHistory)
class ActivityHistoryAdmin(admin.ModelAdmin):
    list_display = ['Instance', 'Contract', 'description',]
"""

# admin.site.register(Instance, InstanceAdmin)
# admin.site.register(ModelType)
admin.site.register(Manufacturer)
# admin.site.register(ScrapRequest)
# admin.site.register(branchSite)
# admin.site.register(ActivityHistory)
