from django.contrib import admin

from .models import Instance, ModelType, Manufacturer

# Register your models here.

admin.site.register(ModelType)
admin.site.register(Instance)
admin.site.register(Manufacturer)