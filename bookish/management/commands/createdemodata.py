from django.core.management.base import BaseCommand
import bookish.models as m
from django.contrib.auth.models import User
import datetime
import csv
from decimal import Decimal


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

        business_year = m.BusinessYear.objects.create(company=company, start_date=datetime.date(2014, 2, 1))

        def import_csv(filename, transaction_type, start_row, end_row):
            with open(filename) as fp:
                sheet = csv.reader(fp)
                for i, row in enumerate(sheet):
                    if i >= start_row and i <= end_row:
                        transaction = m.Transaction.objects.create(company=company, transaction_type=transaction_type)
                        date_values = [int(x) for x in row[0].split('/')]
                        m.TransactionRevision.objects.create(
                            user=demo_client,
                            transaction=transaction,
                            business_year=business_year,
                            name=row[1],
                            date=datetime.date(date_values[2], date_values[1], date_values[0]),
                            amount=row[6] or -Decimal(row[9] if row[9] else 0)
                            #notes='Coffee',
                            #customer_ref='D&W Enterprise',
                            #my_ref="01/893-DW", is_expense=0
                            )

        import_csv('bookish/management/demodata/demo-cash.csv', 'C', 3, 68)
        import_csv('bookish/management/demodata/demo-bank.csv', 'B', 5, 181)
