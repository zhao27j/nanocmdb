from django.contrib import admin

from .models import Contract, PaymentTerm, LegalEntity, Prjct

# Register your models here.

class PaymentTermInline(admin.TabularInline):
    '''Tabular Inline View for '''

    model = PaymentTerm
    # min_num = 3
    # max_num = 20
    extra = 1
    # raw_id_fields = (,)

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['briefing', 'get_parties_display', 'get_prjct', 'type', 'get_total_amount', 'get_contract_duration_in_month', 'get_contract_time_remaining_in_percent']
    autocomplete_fields = ['party_a_list', 'party_b_list', 'assets', ]
    inlines = [PaymentTermInline, ]

@admin.register(LegalEntity)
class LegalEntityAdmin(admin.ModelAdmin):
    search_fields = ['name', ]

# admin.site.register(Contract)
admin.site.register(PaymentTerm)
# admin.site.register(LegalEntity)
admin.site.register(Prjct)