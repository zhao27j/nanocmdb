from django.contrib import admin

from .models import UserProfile, UserDept, SubCategory, ChangeHistory, UploadedFile

# Register your models here.

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['on', 'by', 'db_table_name', 'db_table_pk', 'digital_copy',]


@admin.register(ChangeHistory)
class ChangeHistoryAdmin(admin.ModelAdmin):
    list_display = ['on', 'by', 'db_table_name', 'db_table_pk', 'detail',]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'dept', 'work_phone', 'postal_addr', 'cellphone', 'legal_entity']

    search_fields = ['user__username']
    

# admin.site.register(UserProfile)
admin.site.register(SubCategory)
admin.site.register(UserDept)
# admin.site.register(UploadedFile)