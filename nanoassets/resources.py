from django.contrib.auth.models import User

from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import Instance, ModelType, branchSite, Configuragion


class InstanceResource(resources.ModelResource):
    hostname = fields.Field(
        attribute='configuragion',
        column_name='Hostname',
        widget=ForeignKeyWidget(Configuragion, field='hostname'),
    )
    
    site = fields.Field(
        attribute='branchSite',
        column_name='Site',
        widget=ForeignKeyWidget(branchSite, field='name'),
    )

    model_type = fields.Field(
        attribute='model_type',
        column_name='Model / Type',
        widget=ForeignKeyWidget(ModelType, field='name'),
    )

    username = fields.Field(
        attribute='owner',
        column_name='Username',
        widget=ForeignKeyWidget(User, field='username'),
    )
    user_first_name = fields.Field(
        attribute='owner',
        column_name='First Name',
        widget=ForeignKeyWidget(User, field='first_name'),
    )

    user_last_name = fields.Field(
        attribute='owner',
        column_name='Last Name',
        widget=ForeignKeyWidget(User, field='last_name'),
    )

    user_email = fields.Field(
        attribute='owner',
        column_name='Email',
        widget=ForeignKeyWidget(User, field='email'),

    )

    class Meta:
        model = Instance
        import_id_fields = ('serial_number',)
        skip_unchanged = True
        report_skipped = False
        # exclude = ('eol_date')
        fields = ('serial_number', 'model_type', 'status', 'hostname', 'username', 'user_first_name', 'user_last_name', 'user_email', 'site', 'eol_date')
