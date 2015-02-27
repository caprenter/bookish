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
