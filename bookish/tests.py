from django.contrib.auth.models import User
import bookish.models as m
import bookish.views as v
import uuid
import datetime
import pytest
from decimal import Decimal
from django.core.management import call_command


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
    response = client.post('/cash/edit/', {
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


@pytest.mark.django_db
def test_company_name_is_present(client):
    user = User.objects.create_user(username='test_user', password='password')
    client.login(username='test_user', password='password')
    accountancy_firm = m.AccountancyFirm.objects.create()
    company = m.Company.objects.create(accountancy_firm=accountancy_firm, name="Test Company")
    company.users.add(user)
    response = client.get("/")
    assert response.status_code == 200
    assert "Test Company" in str(response.content)


def setup_view(view, request, *args, **kwargs):
    """Mimic as_view() returned callable, but returns view instance.

    args and kwargs are the same you would pass to ``reverse()``

    function snippet from http://tech.novapost.fr/django-unit-test-your-views-en.html

    """
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


@pytest.mark.django_db
@pytest.mark.parametrize('View', [v.HomePageView, v.TransactionListView, v.TransactionEdit, v.TransactionItemRevisionView, v.AccountancyFirmListView, v.CompanyListView])
#  TODO: We can parametrize these Views to have an appropriate URL to test against: http://pytest.org/latest/parametrize.html
def test_company_name_is_present_unit(View, rf):
    user = User.objects.create_user(username='test_user', password='password')
    accountancy_firm = m.AccountancyFirm.objects.create()
    company = m.Company.objects.create(accountancy_firm=accountancy_firm, name="Test Company")
    company.users.add(user)
    request = rf.get('/')
    request.user = user
    view = View()
    setup_view(view, request)
    assert view.get_company().name == "Test Company"


@pytest.mark.django_db
def test_createdemodata():
    call_command('createdemodata')
    # Look for transactions with a certain date
    revisions = m.TransactionRevision.objects.filter(
        transaction__transaction_type='M',
        date=datetime.date(2014, 2, 17)
    )
    # We only expect one mileage transaction with this date in our demo data
    assert len(revisions) == 1
    revision = revisions[0]
    # Check that the data has been imported correctly
    revision.transaction.transaction_type == 'M'
    revision.amount == Decimal('12.1')


@pytest.mark.xfail
@pytest.mark.django_db
def test_createdemodata_invoice():
    call_command('createdemodata')
    revisions = m.TransactionRevision.objects.filter(
        transaction__transaction_type='C',
        date=datetime.date(2014, 2, 17)
    )
    # We only expect one mileage transaction with this date in our demo data
    assert len(revisions) == 1
    revision = revisions[0]
    # Check that the data has been imported correctly
    revision.transaction.transaction_type == 'C'
    revision.amount == Decimal('12.1')
