from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from django.contrib.auth.models import User

from .models import NonPayrollExpense

class NonPayrollExpenseResource(resources.ModelResource):

    created_by = fields.Field(attribute='created_by', column_name='created_by', widget=ForeignKeyWidget(User, field='username'),)
    
    def before_import_row(self, row, row_number=None, **kwargs):
        pass

    class Meta:
        model = NonPayrollExpense

        # import_id_fields = ('description',)   # 指定 primary key field
        skip_unchanged = True
        report_skipped = False
        # exclude = ('vendor', )
        # fields = ('non_payroll_expense_year', 'non_payroll_expense_reforecasting', 'originating_sub_region', 'functional_department', 'global_gl_account', 'vendor', 'global_expense_tracking_id', 'currency', 'allocation', 'description','jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'is_direct_cost', 'created_by', )