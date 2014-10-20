from django.db import models
from django.contrib.auth.models import User
import uuid


def make_uuid():
    return str(uuid.uuid4())


class UUIDModel(models.Model):
    uuid = models.CharField(max_length=36, primary_key=True, default=make_uuid, editable=False)

    class Meta:
        abstract = True


class Revision(UUIDModel):
    """This class specifies the metadata of the revision."""
    revision_datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)


class AccountancyFirm(UUIDModel):
    users = models.ManyToManyField(User)


class Company(UUIDModel):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User)
    accountancy_firm = models.ForeignKey(AccountancyFirm)


class NominalCode(UUIDModel):
    name = models.CharField(max_length=50)
    companies = models.ManyToManyField(Company)
    accountancy_firm = models.ForeignKey(AccountancyFirm)


class BusinessYear(UUIDModel):
    company = models.ForeignKey(Company)
    start_date = models.DateField()


class Transaction(UUIDModel):
    company = models.ForeignKey(Company)
    transaction_type = models.CharField(max_length=1, choices=(
        ('B', 'Bank'),
        ('C', 'Cash'),
    ))

    def latest_revision(self):
        return self.transactionrevision_set.order_by('-revision_datetime').first()


class TransactionRevision(Revision):
    transaction = models.ForeignKey(Transaction)

    name = models.CharField(max_length=100)
    business_year = models.ForeignKey(BusinessYear)
    date = models.DateField(null=True)
    originating_account = models.CharField(max_length=50, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    nominal_code = models.ForeignKey(NominalCode, null=True, blank=True)
    notes = models.TextField(default='', blank=True)
