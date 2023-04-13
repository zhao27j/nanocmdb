from django.contrib.auth.models import User

from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import Instance, ModelType, branchSite, Configuragion


class InstanceResource(resources.ModelResource):
    hostname = fields.Field(
        column_name='hostname',
        attribute='hostname',
        widget=ForeignKeyWidget(Configuragion, field='hostname'),
    )
    
    site_branch = fields.Field(
        column_name='site',
        attribute='site',
        widget=ForeignKeyWidget(branchSite, field='name'),
    )

    model_type = fields.Field(
        column_name='model_type',
        attribute='model_type',
        widget=ForeignKeyWidget(ModelType, field='name'),
    )

    owner = fields.Field(
        column_name='owner',
        attribute='owner',
        widget=ForeignKeyWidget(User, field='username'),
    )

    class Meta:
        model = Instance
        import_id_fields = ('serial_number',)
        skip_unchanged = True
        report_skipped = False
        # exclude = ('eol_date')
        fields = ('model_type','serial_number', 'hostname', 'status', 'owner', 'site', 'eol_date',)
