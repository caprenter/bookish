import pytest
import os
from selenium import webdriver


@pytest.fixture(scope="module")
def browser(request):
    if 'USE_CHROME' in os.environ:
        browser = webdriver.Chrome()
    else:
        browser = webdriver.Firefox()
    browser.implicitly_wait(3)
    request.addfinalizer(lambda: browser.quit())
    return browser


def test_admin_page_is_shown(live_server, browser):
    # Gertrude opens her web browser, and goes to the admin page
    browser.get(live_server.url + '/admin/')

    # She sees the familiar 'Django administration' heading
    body = browser.find_element_by_tag_name('body')
    assert 'Django administration' in body.text


def test_log_in_link_is_shown(live_server, browser):
    # Ben opens his browser and goes to the main page
    browser.get(live_server.url + '/')

    # He can see a link to log in
    body = browser.find_element_by_tag_name('body')
    assert 'Log in' in body.text
