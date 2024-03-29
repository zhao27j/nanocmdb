from django.contrib import admin

from import_export.admin import ImportExportModelAdmin, ImportMixin

from .resources import NonPayrollExpenseResource
from .models import PaymentRequest, NonPayrollExpense, PaymentTerm, Contract, LegalEntity, Prjct

# Register your models here.

@admin.register(NonPayrollExpense)
class NonPayrollExpenseAdmin(ImportMixin, admin.ModelAdmin):
    resource_classes = [NonPayrollExpenseResource]
    
    list_display = ['non_payroll_expense_year', 'non_payroll_expense_reforecasting', 
                    'originating_sub_region', 'functional_department', 'global_gl_account', 
                    'vendor', 'global_expense_tracking_id', 'currency', 'allocation', 'description', 
                    'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    list_filter = ['non_payroll_expense_year', 'non_payroll_expense_reforecasting', 'allocation',]
    search_fields = ['non_payroll_expense_year', 'non_payroll_expense_reforecasting', 'allocation', 'description', ]

@admin.register(PaymentRequest)
class PaymentRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'amount', 'non_payroll_expense', 'requested_on', 'requested_by', 'IT_reviewed_on', 'IT_reviewed_by']

class PaymentTermInline(admin.TabularInline):
    # Tabular Inline View for
    model = PaymentTerm
    # min_num = 3
    # max_num = 20
    extra = 1
    # raw_id_fields = (,)

@admin.register(PaymentTerm)
class PaymentTermAdmin(admin.ModelAdmin):
    list_display = ['contract', 'pay_day', 'plan', 'recurring', 'amount', 'applied_on']


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['briefing', 'get_parties_display', 'get_prjct', 'type', 'get_total_amount', 'get_duration_in_month', 'get_time_remaining_in_percent']
    autocomplete_fields = ['party_a_list', 'party_b_list', 'assets', ]
    inlines = [PaymentTermInline, ]

@admin.register(LegalEntity)
class LegalEntityAdmin(admin.ModelAdmin):
    search_fields = ['name', ]


# admin.site.register(PaymentRequest)
#admin.site.register(PaymentTerm)
# admin.site.register(Contract)
# admin.site.register(LegalEntity)
admin.site.register(Prjct)
