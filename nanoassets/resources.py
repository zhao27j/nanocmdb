from django.contrib.auth.models import User

from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import Instance, ModelType

class InstanceResource(resources.ModelResource):
    model_type = fields.Field(
        column_name='model_type',
        attribute='model_type',
        widget=ForeignKeyWidget(ModelType, field='name'),
    )
    
    owner =fields.Field(
        column_name='owner',
        attribute='owner',
        widget=ForeignKeyWidget(User, field='username'),
    )

    class Meta:
        model = Instance
        # fields = ('model_type')
