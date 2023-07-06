from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
        return True if group in user.groups.all() else False
    except:
        return False


@register.filter(name='grouped_by_sub_category')
def grouped_by_sub_category(instance_list, sub_category):
    try:
        instance_list_grouped_by_sub_category = instance_list.filter(model_type__sub_category=sub_category)
        return instance_list_grouped_by_sub_category if instance_list_grouped_by_sub_category else None
    except:
        return False
    

@register.filter(name='grouped_by_sub_category_count')
def grouped_by_sub_category_count(instance_list, sub_category):
    try:
        instance_list_grouped_by_sub_category_count = instance_list.filter(model_type__sub_category=sub_category).count()
        return instance_list_grouped_by_sub_category_count if instance_list_grouped_by_sub_category_count else None
    except:
        return False