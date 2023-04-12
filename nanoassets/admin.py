from django.contrib import admin

from import_export.admin import ImportExportModelAdmin, ImportExportMixin

from .resources import InstanceResource
from .models import Instance, ModelType, Manufacturer, ScrapRequest, branchSite

# Register your models here.


@admin.register(ScrapRequest)
class ScrapRequestAdmin(admin.ModelAdmin):
    list_display = ['case_id', 'status', 'requested_by', 'requested_on', 'approved_by', 'approved_on',]


@admin.register(Instance)
class InstanceAdmin(ImportExportModelAdmin):
    resource_classes = [InstanceResource]

    list_display = ['serial_number', 'model_type', 'status', 'eol_date', 'owner', 'branchSite', 'scrap_request']
    # list_filter = ['model_type', 'status']
    search_fields = ['model_type__name', 'status', 'owner__username', 'eol_date']


@admin.register(branchSite)
class branchSiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_onSiteTech', 'city', 'addr',]
    autocomplete_fields = ['country',]

# admin.site.register(Instance, InstanceAdmin)
admin.site.register(ModelType)
admin.site.register(Manufacturer)
# admin.site.register(ScrapRequest)
# admin.site.register(branchSite)
