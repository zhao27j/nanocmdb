from io import BytesIO
import datetime
import pathlib

from typing import Any, Dict

from django.core.files import File
from django.core.mail import EmailMessage
from django.utils import timezone

from django.http import HttpResponse, Http404, FileResponse
from django.template.loader import get_template, render_to_string
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy

from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.views import generic
from django.views.generic.edit import CreateView

from .models import LegalEntity, Contract, PaymentTerm, PaymentRequest, NonPayrollExpense
from .forms import NewContractForm, NewPaymentTermForm, NewPaymentRequestForm

# Create your views here.

def payment_request_paper_form(request, pk):
    payment_request = get_object_or_404(PaymentRequest, pk=pk)

    # contract = payment_request.payment_term.contract
    contract_accumulated_payment_excluded_this_request = 0
    accumulated_payment_excluded_this_request = 0
    for paymentTerm in PaymentTerm.objects.filter(contract=payment_request.payment_term.contract):
        if paymentTerm.paymentrequest_set.all():
            for payment_req in paymentTerm.paymentrequest_set.all():
                if paymentTerm.applied_on < payment_request.requested_on:
                    contract_accumulated_payment_excluded_this_request += payment_req.amount
                    if paymentTerm.applied_on.year == payment_request.non_payroll_expense.non_payroll_expense_year:
                        accumulated_payment_excluded_this_request += payment_req.amount

    context = {
        "payer": payment_request.payment_term.contract.get_party_a_display(),
        "date_of_request": payment_request.requested_on,
        "payment_due_date": '',
        "contract_amount": payment_request.non_payroll_expense.get_currency_display() + "{:,.2f}".format(payment_request.payment_term.contract.get_total_amount()['amount__sum']),
        # "contract_accumulated_payment_excluded_this_request": payment_request.non_payroll_expense.get_currency_display() + "{:,.2f}".format(payment_request.payment_term.contract.get_total_amount_applied()['amount__sum']),
        "contract_accumulated_payment_excluded_this_request": payment_request.non_payroll_expense.get_currency_display() + "{:,.2f}".format(contract_accumulated_payment_excluded_this_request),
        "included_in_the_budget_yes": '✔️',
        "included_in_the_budget_no": '☐',
        "budget_dept_code_budget_originator": payment_request.non_payroll_expense.functional_department,
        "budget_expense_category_major_and_minor": payment_request.non_payroll_expense.global_gl_account,
        "total_budget_amount_in_gbs_minor_category": payment_request.non_payroll_expense.get_currency_display() + "{:,.2f}".format(payment_request.non_payroll_expense.get_non_payroll_expense_subtotal()),
        "accumulated_payment_excluded_this_request": payment_request.non_payroll_expense.get_currency_display() + "{:,.2f}".format(accumulated_payment_excluded_this_request),
        "remaining_budget_after_this_payment": '',
        "job_code": payment_request.non_payroll_expense.global_expense_tracking_id,
        "item_1_description": payment_request.non_payroll_expense.description,
        "item_1_amount": payment_request.non_payroll_expense.get_currency_display() + "{:,.2f}".format(payment_request.amount),
        "item_1_allocation_code": payment_request.non_payroll_expense.allocation,
        "item_1_allocation_percentage": '100%',
        "item_1_allocated_amount": payment_request.non_payroll_expense.get_currency_display() + "{:,.2f}".format(payment_request.amount),
        "total_amount": payment_request.non_payroll_expense.get_currency_display() + "{:,.2f}".format(payment_request.amount),
        "total_allocated_amount": payment_request.non_payroll_expense.get_currency_display() + "{:,.2f}".format(payment_request.amount),
        "transfer_petty_cash": "☐",
        "transfer_check": "☐",
        "transfer_wire": "✔️",
        "payee": payment_request.payment_term.contract.get_party_b_display(),
        "bank_information_deposit": payment_request.payment_term.contract.party_b_list.first().deposit_bank,
        "bank_information_deposit_account": payment_request.payment_term.contract.party_b_list.first().deposit_bank_account,
    }
    path = "nanopay/payment_request_paper_form.html" # find the template and render it.
    template = get_template(path)
    html = template.render(context)
    return HttpResponse(html)


@login_required
def payment_request_approved(request, pk):
    payment_request = get_object_or_404(PaymentRequest, pk=pk)
    payment_request.status = 'A'
    payment_request.IT_reviewed_by = request.user
    payment_request.IT_reviewed_on = datetime.date.today()

    payment_request.save()

    payment_request.payment_term.contract.activityhistory_set.create(
        description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' + 
        'the Payment Request [ ' + str(payment_request.id) + ' ] was approved by ' + request.user.get_full_name()
        )
    
    messages.info(request, 'the Approval decision for the Payment Request [ ' + str(payment_request.id) + ' ] was sent')

    message = get_template("nanopay/payment_request_approved_email.html").render({
        'protocol': 'http',
        'domain': '127.0.0.1:8000',
        'payment_request': payment_request,
    })
    mail = EmailMessage(
        subject='ITS express - Please noticed - Payment Request approved by ' + payment_request.requested_by.get_full_name(),
        body=message,
        from_email='nanoMessenger <do-not-reply@tishmanspeyer.com>',
        to=[payment_request.requested_by.email],
        cc=[request.user.email],
        # reply_to=[EMAIL_ADMIN],
        # connection=
    )
    mail.content_subtype = "html"
    mail.send()

    # return redirect('nanopay:contract-detail', pk=payment_request.payment_term.contract.pk) # redirect to a new URL:
    return redirect('nanopay:payment-request-list')


class PaymentRequestDetailView(LoginRequiredMixin, generic.DetailView):
    model = PaymentRequest


@login_required
def payment_request_detail_invoice_scanned_copy(request, pk):
    payment_request = get_object_or_404(PaymentRequest, pk=pk)
    invoice_scanned_copy_path = payment_request.scanned_copy.name
    try:
        invoice_scanned_copy = open(invoice_scanned_copy_path, 'rb')
        return FileResponse(invoice_scanned_copy, content_type='application/pdf')
    except FileNotFoundError:
        raise Http404


class PaymentRequestListView(LoginRequiredMixin, generic.ListView):
    model = PaymentRequest
    template_name = 'nanopay/payment_request_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def payment_request_new(request, pk):
    payment_term = get_object_or_404(PaymentTerm, pk=pk)
    if payment_term.contract.assets.first() == None:
        messages.info(request, 'please associated IT Assets with the Contract [ ' + payment_term.contract.briefing + ' ]')
        # return redirect(request.path) # 重定向 至 当前 页面 (不合适)
        return redirect('nanopay:contract-detail', pk=payment_term.contract.pk)
    non_payroll_expenses = NonPayrollExpense.objects.all()
    if request.method == 'POST':
        form = NewPaymentRequestForm(request.POST, request.FILES)
        if form.is_valid():
            new_payment_request = PaymentRequest.objects.create(
                requested_by=request.user,
                payment_term=payment_term,
                # times=times,
                non_payroll_expense=get_object_or_404(NonPayrollExpense, description=form.cleaned_data['non_payroll_expense']),
                amount=form.cleaned_data.get('amount'),
                )
            new_payment_request.scanned_copy = form.cleaned_data['scanned_copy']
            
            new_payment_request.save()

            payment_term.applied_on = new_payment_request.requested_on
            payment_term.save()

            payment_term.contract.activityhistory_set.create(
                description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' + 
                'the Payment Request [ ' + str(new_payment_request.id) + ' ] was submitted by ' + request.user.get_full_name()
                )
            
            messages.info(request, 'the notification for the Payment Request [ ' + str(new_payment_request.id) + ' ] was sent')

            IT_reviewer_emails = []
            for reviewer in User.objects.filter(groups__name='IT Reviewer'):
                IT_reviewer_emails.append(reviewer.email)

            message = get_template("nanopay/payment_request_new_email.html").render({
                'protocol': 'http',
                'domain': '127.0.0.1:8000',
                'new_payment_request': new_payment_request,
            })
            mail = EmailMessage(
                subject='ITS express - Please approve - Payment Request submitted by ' + new_payment_request.requested_by.get_full_name(),
                body=message,
                from_email='nanoMessenger <do-not-reply@tishmanspeyer.com>',
                to=IT_reviewer_emails,
                cc=[request.user.email],
                # reply_to=[EMAIL_ADMIN],
                # connection=
            )
            mail.content_subtype = "html"
            mail.send()

            return redirect('nanopay:contract-detail', pk=payment_term.contract.pk) # redirect to a new URL:
            # return redirect(request.META.get('HTTP_REFERER')) # 重定向 至 前一个 页面 (在此不适合)
    else:
        payment_term_last = PaymentTerm.objects.filter(contract=payment_term.contract).order_by("applied_on").last()
        
        # payment_request_last = PaymentRequest.objects.filter(payment_term__pk=payment_term.pk).order_by("requested_on").last()
        if payment_term_last:
            non_payroll_expense_last = payment_term_last.paymentrequest_set.first().non_payroll_expense
        else:
            non_payroll_expense_last = ""
        form = NewPaymentRequestForm(
            initial={
                'amount': payment_term.amount,
                'non_payroll_expense': non_payroll_expense_last,
            })

    return render(request, 'nanopay/payment_request_new.html', {
        'form': form,
        'non_payroll_expenses': non_payroll_expenses,
        'payment_term': payment_term,
        })


@login_required
def new_payment_term(request, pk):
    contract = get_object_or_404(Contract, pk=pk)
    if request.method == 'POST': # if this is a POST request then process the Form data
        post = request.POST.copy()
        post['contract'] = contract
        form = NewPaymentTermForm(post) # create a form instance and populate it with data from the request (binding):
        # form.save(commit=False)
        if form.is_valid(): # check if the form is valid:
            # process the data in form.cleaned_data as required
            new_payment_term_plan = form.cleaned_data['plan']
            new_payment_term_recurring = form.cleaned_data['recurring']
            if new_payment_term_plan != 'C' and new_payment_term_recurring > 1:
                pay_day = form.cleaned_data['pay_day']
                recurring = 1
                while recurring < new_payment_term_recurring:
                    if new_payment_term_plan == 'M':
                        pay_day += datetime.timedelta(weeks=(4.33333))
                    elif new_payment_term_plan == 'Q':
                        pay_day += datetime.timedelta(weeks=(13))
                    elif new_payment_term_plan == 'S':
                        pay_day += datetime.timedelta(weeks=(26))
                    elif new_payment_term_plan == 'A':
                        pay_day += datetime.timedelta(weeks=(52))
                    
                    PaymentTerm.objects.create(pay_day=pay_day, plan=new_payment_term_plan, recurring=1, amount=form.cleaned_data['amount'], contract=form.cleaned_data['contract'],)
                    recurring += 1

            new_payment_term = form.save(commit=False)
            new_payment_term.recurring = 1
            # new_payment_term.contract = contract
            new_payment_term.save()

            contract.activityhistory_set.create(
                description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] '
                  + str(new_payment_term_recurring) + ' x ' + new_payment_term.get_plan_display()
                    + ' Payment Term scheduled since ' + str(new_payment_term.pay_day)
                      + ' in amount ' + str(new_payment_term.amount)
                        + ' were added by ' + request.user.get_full_name()
                )
            
            messages.info(request, 
                          str(new_payment_term_recurring) + ' x ' + new_payment_term.get_plan_display()
                            + 'Payment Terms for the Contract [ ' + contract.briefing
                              + ' ] were added by ' + request.user.get_full_name()
                              )

            return redirect('nanopay:contract-detail', pk=pk) # redirect to a new URL:

    else: # if this is a GET (or any other method) create the default form.
        pay_day = contract.startup + datetime.timedelta(weeks=4.33333)
        form = NewPaymentTermForm(initial={
            'pay_day': pay_day,
            'contract': contract,
            })

    return render(request, 'nanopay/payment_term_new.html', {'form': form,})


@login_required
def contract_detail_scanned_copy(request, pk):
    contract_instance = get_object_or_404(Contract, pk=pk)
    scanned_copy_path = contract_instance.scanned_copy.name
    try:
        scanned_copy = open(scanned_copy_path, 'rb')
        return FileResponse(scanned_copy, content_type='application/pdf')
    except FileNotFoundError:
        raise Http404


@login_required
def new_contract(request):
    if request.method == 'POST': # if this is a POST request then process the Form data
        form = NewContractForm(request.POST, request.FILES) # create a form instance and populate it with data from the request (binding):
        if form.is_valid(): # check if the form is valid:
            # process the data in form.cleaned_data as required
            new_contract = Contract()
            
            new_contract.briefing = form.cleaned_data['briefing']
            
            new_contract.type = form.cleaned_data['type']
            # new_contract.non_payroll_expense = get_object_or_404(NonPayrollExpense, description=form.cleaned_data['non_payroll_expense'])

            new_contract.startup = form.cleaned_data['startup']
            new_contract.endup = form.cleaned_data['endup']
            new_contract.scanned_copy = form.cleaned_data['scanned_copy']
            new_contract.created_by = request.user
            new_contract.save()

            new_contract.party_a_list.set(form.cleaned_data['party_a_list'])
            new_contract.party_b_list.set(form.cleaned_data['party_b_list'])

            new_contract.activityhistory_set.create(
                description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' + 'the base info was added by ' + request.user.get_full_name()
                )
            
            messages.info(request, 'the base info of the new Contract [ ' + form.cleaned_data['briefing'] + ' ] was added by ' + request.user.get_full_name())


            # return redirect(new_contract.get_absolute_url()) # redirect to a new URL:
            return redirect('nanopay:payment-term-new', pk=new_contract.pk)

    else: # if this is a GET (or any other method) create the default form.
        startup = datetime.date.today()
        endup = datetime.date.today() + datetime.timedelta(weeks=12)
        # non_payroll_expenses = NonPayrollExpense.objects.all()
        
        form = NewContractForm(
            initial={
                'startup': startup,
                'endup': endup,
                })
        return render(request, 'nanopay/contract_new.html', {
            'form': form,
            # 'non_payroll_expenses': non_payroll_expenses,
            })

    return render(request, 'nanopay/contract_new.html', {'form': form,})


class ContractListView(LoginRequiredMixin, generic.ListView):
    model = Contract
    # paginate_by = 10

    """
    def get_queryset(self):
        return super().get_queryset()
    """


class ContractDetailView(LoginRequiredMixin, generic.DetailView):
    model = Contract
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.paymentterm_set.all():
            payment_term = self.object.paymentterm_set.all().first()
            if payment_term.paymentrequest_set.all():
                payment_request = payment_term.paymentrequest_set.all().first()
                non_payroll_expense = payment_request.non_payroll_expense
                context["non_payroll_expense"] = non_payroll_expense
            else:
                context["non_payroll_expense"] = '[yet associated]'
        else:
            context["non_payroll_expense"] = '[yet associated]'
        return context