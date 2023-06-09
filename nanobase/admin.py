from django.contrib import admin

from .models import UserProfile, UserDept, SubCategory

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'dept', 'work_phone', 'postal_addr', 'cellphone', 'legal_entity']
    

# admin.site.register(UserProfile)
admin.site.register(SubCategory)
admin.site.register(UserDept)