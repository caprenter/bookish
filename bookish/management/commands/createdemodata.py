from django.core.management.base import BaseCommand
import bookish.models as m
from django.contrib.auth.models import User
import datetime


class Command(BaseCommand):
    help = 'Creates bookish demo data'

    def handle(self, *args, **options):
        User.objects.create_superuser(username='demo_admin', password='demo_admin', email='demo@example.org')
        demo_accountant = User.objects.create(username='demo_accountant', password='demo_accountant')
        demo_client = User.objects.create(username='demo_client', password='demo_client')

        accountancy_firm = m.AccountancyFirm.objects.create()
        accountancy_firm.users.add(demo_accountant)

        company = m.Company.objects.create(name="Demo Company", accountancy_firm=accountancy_firm)
        company.users.add(demo_client)

        m.BusinessYear.objects.create(company=company, start_date=datetime.date(2014, 4, 1))
