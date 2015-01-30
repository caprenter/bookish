from django.contrib.auth.models import User
import bookish.models as m
import uuid
import datetime
import pytest

class UUIDModelSubClass(m.UUIDModel):
    pass

@pytest.mark.django_db
def test_uuid():
    UUIDModelSubClass.objects.create()
    uuid_model_object = UUIDModelSubClass.objects.all()[0]
    # Check that the uuid field is being used as the pk
    assert uuid_model_object.pk == uuid_model_object.uuid
    # Check that the uuid field is a valid uuid by attempting to create a
    # UUID object with it.
    uuid.UUID(uuid_model_object.uuid)

@pytest.mark.django_db
def test_create_cash(client):
    user = User.objects.create_user(username='test_user', password='password')
    client.login(username='test_user', password='password')
    accountancy_firm = m.AccountancyFirm.objects.create()
    company = m.Company.objects.create(accountancy_firm=accountancy_firm)
    company.users.add(user)
    business_year = m.BusinessYear.objects.create(company=company, start_date=datetime.date(2014, 4, 1))
    response = client.post('/cash/edit', {
        'name': 'Test',
        'business_year': str(business_year.pk),
        'date': '2014-01-01',
        'amount': '1'
        })
    assert response.status_code == 302
    assert response.url == 'http://testserver/cash'
    assert len(m.Transaction.objects.all()) == 1
    transaction = m.Transaction.objects.first()
    assert transaction.company == company
    assert transaction.latest_revision().name == 'Test'
    assert transaction.latest_revision().date == datetime.date(2014, 1, 1)
    assert transaction.latest_revision().amount == 1
    assert transaction.latest_revision().business_year == business_year
