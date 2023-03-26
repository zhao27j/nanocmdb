from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .resources import InstanceResource
from .models import Instance, ModelType, Manufacturer

# Register your models here.

class InstanceAdmin(ImportExportModelAdmin):
    resource_classes = [InstanceResource]

admin.site.register(Instance, InstanceAdmin)
admin.site.register(ModelType)
admin.site.register(Manufacturer)