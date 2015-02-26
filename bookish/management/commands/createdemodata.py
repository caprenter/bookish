from django.core.management.base import BaseCommand
import bookish.models as m
from django.contrib.auth.models import User
import datetime


class Command(BaseCommand):
    help = 'Creates bookish demo data'

    def handle(self, *args, **options):
        User.objects.create_superuser(username='demo_admin', password='demo_admin', email='demo@example.org')
        demo_accountant = User.objects.create_user(username='demo_accountant', password='demo_accountant')
        demo_client = User.objects.create_user(username='demo_client', password='demo_client')

        accountancy_firm = m.AccountancyFirm.objects.create()
        accountancy_firm.users.add(demo_accountant)

        company = m.Company.objects.create(name="Demo Company", accountancy_firm=accountancy_firm)
        company.users.add(demo_client)

        business_year = m.BusinessYear.objects.create(company=company, start_date=datetime.date(2014, 4, 1))

        #Demo Receipt for demo_client
        demo_receipt = m.Transaction.objects.create(company=company, transaction_type='R')
        m.TransactionRevision.objects.create(user=demo_client, transaction=demo_receipt, name='Demo Receipt', business_year=business_year, date=datetime.date(2014, 6, 10), amount=4.97, notes='Coffee', customer_ref='D&W Enterprise', my_ref="01/893-DW", is_expense=0)   # missing nominal code
