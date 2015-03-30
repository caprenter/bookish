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
                    #if i >= start_row and i <= 25:  #use this to only import a few lines of the demo data for faster import
                    if i >= start_row and i <= end_row:
                        transaction = m.Transaction.objects.create(company=company, transaction_type=transaction_type)
                        date_values = [int(x) for x in row[0].split('/')]
                        transaction_revision = m.TransactionRevision(
                            user=demo_client,
                            transaction=transaction,
                            business_year=business_year,
                            name=row[1],
                            date=datetime.date(date_values[2], date_values[1], date_values[0]),
                            
                            #nominal_code = m.NominalCode
                            #additional_information=row[4] if transaction_type == 'B' else '',
                            #customer_ref=row[3],
                            #customer_ref: Receipt.CustomerRef, Cash In.CustomerRef, Bank.CustomerRef,	Milage.CustomerRef
                            #my_ref=row[2],
                            # is_expense=0
                        )
                        if transaction_type == 'B':
                            transaction_revision.my_ref = row[2]
                            transaction_revision.additional_information = row[4]
                            transaction_revision.customer_ref = row[3]
                            transaction_revision.supplier_invoice = row[13]
                            transaction_revision.amount = row[6] or -Decimal(row[9] if row[9] else 0)
                            transaction_revision.is_VAT = 1 if row[5] == 'Y' else 0
                        if transaction_type == 'I':
                            raised_date_values = [int(x) for x in row[3].split('/')]
                            raised_date = datetime.date(raised_date_values[2], raised_date_values[1], raised_date_values[0])
                            transaction_revision.raised_date = raised_date
                            transaction_revision.my_ref = row[2]
                            transaction_revision.amount = row[6]
                            transaction_revision.actual_amount = row[7]
                            transaction_revision.notes = row[8]
                        if transaction_type == 'C':
                            transaction_revision.amount = row[6] or -Decimal(row[9] if row[9] else 0)
                            transaction_revision.is_expense = 1 if row[2] else 0
                            transaction_revision.is_VAT = 1 if row[5] == 'Y' else 0
                        if transaction_type == 'M':
                            transaction_revision.amount = row[2]
                        
                        # Handle Nominal Codes
                        # Only certain transactions have them
                        transactions_with_nominal_codes = {'B': 14, 'R': 2, 'C': 4}  # Associate the transaction types with the column in the spreadsheat
                        
                        if transaction_type in transactions_with_nominal_codes:
                            # Look up a given value to see if it exists
                            column = transactions_with_nominal_codes[transaction_type]
                            nominal_code = m.NominalCode.objects.filter(name=row[column]).first()
                            #nominal_code = m.NominalCode.objects.create(company=company, accountancy_firm=accountancy_firm, name='des')
                            # If not create it
                            if not nominal_code:
                                nominal_code = m.NominalCode.objects.create(accountancy_firm=accountancy_firm, name=row[column])
                            
                            # Add it to our transaction revision
                            transaction_revision.nominal_code = nominal_code
                                
                        transaction_revision.save()
                        
        import_csv('bookish/management/demodata/demo-cash.csv', 'C', 3, 68)
        import_csv('bookish/management/demodata/demo-bank.csv', 'B', 5, 181)
        import_csv('bookish/management/demodata/demo-mileage.csv', 'M', 1, 28)
        import_csv('bookish/management/demodata/demo-invoices.csv', 'I', 1, 28)
