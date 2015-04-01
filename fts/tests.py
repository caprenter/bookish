import pytest
import os
from selenium import webdriver
from django.contrib.auth.models import User
import bookish.models as m


@pytest.fixture(scope="module")
def browser(request):
    if 'USE_CHROME' in os.environ:
        browser = webdriver.Chrome()
    else:
        browser = webdriver.Firefox()
    browser.implicitly_wait(3)
    request.addfinalizer(lambda: browser.quit())
    return browser


@pytest.fixture(scope="module")
def demo_users(request):
    # Create system users. Minimum is admin, accountant, and a user in a company
    User.objects.create_superuser(username='demo_admin', password='demo_admin', email='demo@example.org')
    demo_accountant = User.objects.create_user(username='demo_accountant', password='demo_accountant')
    demo_client = User.objects.create_user(username='demo_client', first_name="David", last_name="Dangerfield", password='demo_client')
    
    # Create an accountancy firm
    accountancy_firm = m.AccountancyFirm.objects.create(name="ABC Accountants")
    accountancy_firm.users.add(demo_accountant)
    
    # Create a company
    company = m.Company.objects.create(name="Demo Company", accountancy_firm=accountancy_firm, address="21 Happy Gardens, Halifax, W.Yorks, HX1 4RT", VAT_registartion_number="123456789")
    company.users.add(demo_client)


def test_admin_page_is_shown(live_server, browser):
    # Gertrude opens her web browser, and goes to the admin page
    browser.get(live_server.url + '/admin/')

    # She sees the familiar 'Django administration' heading
    body = browser.find_element_by_tag_name('body')
    assert 'Django administration' in body.text


def test_log_in(live_server, browser, demo_users):
    # Ben opens his browser and goes to the main page
    browser.get(live_server.url + '/')

    # He can see a link to log in
    body = browser.find_element_by_tag_name('body')
    assert 'Log in' in body.text

    # He can click the link...
    body.find_element_by_link_text('Log in').click()

    # .. and then submit login details
    browser.find_element_by_id('id_username').send_keys('demo_client')
    browser.find_element_by_id('id_password').send_keys('demo_client')
    browser.find_element_by_css_selector('input[type=submit]').click()
    # He can then see his user name, company name and a link to log out
    body = browser.find_element_by_tag_name('body')
    assert 'Demo Company' in body.text
    assert 'demo_client' in body.text
    assert 'Logout' in body.text
