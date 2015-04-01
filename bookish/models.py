from django.db import models
from django.contrib.auth.models import User
import uuid
import datetime


def make_uuid():
    return str(uuid.uuid4())


class UUIDModel(models.Model):
    uuid = models.CharField(max_length=36, primary_key=True, default=make_uuid, editable=False)
    # mini_uuid = uuid[:2]

    def mini_uuid(self):
        return self.uuid[:8]  # takes you to the first dash in uuid 0a5bcc1a-87e4-4257-9206-7432eaf7fb60

    class Meta:
        abstract = True


class Revision(UUIDModel):
    """This class specifies the metadata of the revision."""
    revision_datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)


class AccountancyFirm(UUIDModel):
    users = models.ManyToManyField(User)
    name = models.CharField(max_length=50)


class Company(UUIDModel):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User)
    accountancy_firm = models.ForeignKey(AccountancyFirm)
    address = models.TextField(default='', blank=True)
    # is_VAT_registered = models.BooleanField(default=0)  # Maybe we don't need this. If registration number given then it is VAT registered
    VAT_registartion_number = models.CharField(max_length=20, blank=True)
    

class NominalCode(UUIDModel):
    name = models.CharField(max_length=50)
    companies = models.ManyToManyField(Company)
    accountancy_firm = models.ForeignKey(AccountancyFirm)


class BankAccount(UUIDModel):
    name = models.CharField(max_length=50)
    account_number = models.CharField(max_length=50)
    account_sort_code = models.CharField(max_length=50)
    company = models.ForeignKey(Company)


class BusinessYear(UUIDModel):
    company = models.ForeignKey(Company)
    start_date = models.DateField()

    def __str__(self):
        return '{} - {}'.format(
            self.start_date.strftime('%b %y'),
            (self.start_date + datetime.timedelta(days=360)).strftime('%b %y')
            )


class VATRate(UUIDModel):
    rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date = models.DateField(null=True)
    
    
class Vehicle(UUIDModel):  # May need to look at recording changes to vehicle records
    name = models.CharField(max_length=50)
    companies = models.ManyToManyField(Company)
    users = models.ManyToManyField(User)
    fuel_type = models.CharField(max_length=2, choices=(
        ('D', 'Deisel'),
        ('P', 'Petrol'),
        ('B', 'Bicycle'),
        ('H', 'Hybrid'),
    ))
    registration_number = models.CharField(max_length=20, blank=True)
    engine_size = models.PositiveSmallIntegerField()
    business_year = models.ManyToManyField(BusinessYear)  # need to record the business years it was used in


class Transaction(UUIDModel):
    company = models.ForeignKey(Company)
    transaction_type = models.CharField(max_length=2, choices=(
        ('B', 'Bank'),
        ('C', 'Cash'),
        ('R', 'Receipt'),
        ('I', 'Invoice'),
        ('M', 'Milage'),
        ('CN', 'Credit Note'),
    ))

    def latest_revision(self):
        return self.transactionrevision_set.order_by('-revision_datetime').first()

    def mini_uuid(self):
        return self.uuid[:8]  # takes you to the first dash in uuid 0a5bcc1a-87e4-4257-9206-7432eaf7fb60


class TransactionRevision(Revision):
    transaction = models.ForeignKey(Transaction)
    ''' Fields map to:
        name: Receipt.Name, Cash In.Name, Bank.Description, Milage.Description, Invoice.Description, Credit Note.Description
        business_year: Business Year (all views)
        date: Date (all views)
        originating_account = ??
        amount: Receipt.Credit&Debit, Cash In.Credit&Debit, Bank.Credit&Debit, Milage.Miles, Invoice.Invoice amount, Credit Note.Credit Amount
        nominal_code: Receipt.NominalCode, Cash In.NominalCode, Bank.NominalCode,	Milage.NominalCode
        notes: Receipt.Notes, Cash In.Notes, Bank.Notes, Milage.Notes, Invoice.Notes
        customer_ref: Receipt.CustomerRef, Bank.CustomerRef,	Milage.CustomerRef
        my_ref: Receipt.My Reference, Cash In.My Receipt No., [Bank.bank reference - removed from view, not sure if we will use it], Invoice.Invoice number, Credit Note.CreditNoteNo.
        actual_amount: Invoce.Amount Paid
        is_expense: Receipt.Expense?
        additional_information: Bank.Additional Information
        supplier_invoice: Bank.Sales/Supplier Invoice, Cash.Sales Invoice
        my_invoice: Credit Note.My/Sales invoice
    '''
    name = models.CharField(max_length=100)
    business_year = models.ForeignKey(BusinessYear)
    date = models.DateField(null=True)
    raised_date = models.DateField(null=True)
    originating_account = models.CharField(max_length=50, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    nominal_code = models.ForeignKey(NominalCode, null=True, blank=True)
    notes = models.TextField(default='', blank=True)
    customer_ref = models.CharField(max_length=100, blank=True)
    my_ref = models.CharField(max_length=100, blank=True)
    actual_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_expense = models.BooleanField(default=0)
    is_VAT = models.BooleanField(default=0, blank=True)
    additional_information = models.CharField(max_length=100, blank=True)
    supplier_invoice = models.CharField(max_length=100, blank=True)
    my_invoice = models.ForeignKey(Transaction, related_name='my_sales_invoice', null=True)
    #state = still needs to be added
