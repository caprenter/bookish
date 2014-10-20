from django.test import TestCase
from django.contrib.auth.models import User
import bookish.models as m
import uuid
import datetime


class UUIDModelSubClass(m.UUIDModel):
    pass


class UUIDTestCase(TestCase):
    def setUp(self):
        UUIDModelSubClass.objects.create()

    def test_uuid(self):
        uuid_model_object = UUIDModelSubClass.objects.all()[0]
        # Check that the uuid field is being used as the pk
        self.assertEqual(uuid_model_object.pk, uuid_model_object.uuid)
        # Check that the uuid field is a valid uuid by attempting to create a
        # UUID object with it.
        uuid.UUID(uuid_model_object.uuid)


class CashTestCase(TestCase):
    def test_create(self):
        user = User.objects.create_user(username='test_user', password='password')
        self.client.login(username='test_user', password='password')
        accountancy_firm = m.AccountancyFirm.objects.create()
        company = m.Company.objects.create(accountancy_firm=accountancy_firm)
        company.users.add(user)
        business_year = m.BusinessYear.objects.create(company=company, start_date=datetime.date(2014, 4, 1))
        response = self.client.post('/cash/edit', {
            'name': 'Test',
            'business_year': str(business_year.pk),
            'date': '2014-01-01',
            'amount': '1'
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://testserver/cash')
        self.assertEqual(len(m.Transaction.objects.all()), 1)
        transaction = m.Transaction.objects.first()
        self.assertEqual(transaction.company, company)
        self.assertEqual(transaction.latest_revision().name, 'Test')
        self.assertEqual(transaction.latest_revision().date, datetime.date(2014, 1, 1))
        self.assertEqual(transaction.latest_revision().amount, 1)
        self.assertEqual(transaction.latest_revision().business_year, business_year)
