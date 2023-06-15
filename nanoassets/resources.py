from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from django.contrib.auth.models import User

from .models import Instance, ModelType, branchSite

class InstanceResource(resources.ModelResource):
    model_type = fields.Field(attribute='model_type', column_name='Model / Type', widget=ForeignKeyWidget(ModelType, field='name'),)
    
    # hostname = fields.Field(attribute='configuragion', column_name='Hostname', widget=ForeignKeyWidget(Configuragion, field='hostname'),)

    owner = fields.Field(attribute='owner', column_name='Owner', widget=ForeignKeyWidget(User, field='username'),)

    site = fields.Field(attribute='branchSite', column_name='Site', widget=ForeignKeyWidget(branchSite, field='name'),)

    def before_import_row(self, row, row_number=None, **kwargs):
        if str(row["Model / Type"]).strip():
            model_type_name = str(row["Model / Type"]).strip()
            ModelType.objects.get_or_create(name=model_type_name, defaults={"name": model_type_name})

        """
        if str(row["Hostname"]).strip():
            configuragion_hostname = str(row["Hostname"]).strip()
            Configuragion.objects.get_or_create(hostname=configuragion_hostname, defaults={"hostname": configuragion_hostname})
        """

        if str(row["Owner"]).strip():
            owner_username = str(row["Owner"]).strip().lower()
            owner_first_name = str(row["First Name"]).strip().capitalize()
            owner_last_name = str(row["Last Name"]).strip().capitalize()
            owner_email = str(row["Email"]).strip()
            User.objects.get_or_create(username=owner_username, defaults={
                "username": owner_username,
                "first_name": owner_first_name,
                "last_name": owner_last_name,
                "email": owner_email,
                })

        if str(row["Site"]).strip():
            site_name = str(row["Site"]).strip()
            branchSite.objects.get_or_create(name=site_name, defaults={"name": site_name})

        return super().before_import_row(row, row_number, **kwargs)

    class Meta:
        model = Instance
        import_id_fields = ('serial_number',)
        skip_unchanged = True
        report_skipped = False
        # exclude = ('eol_date')
        fields = ('serial_number', 'model_type', 'status', 'hostname', 'owner', 'user_first_name', 'user_last_name', 'user_email', 'site', 'eol_date')