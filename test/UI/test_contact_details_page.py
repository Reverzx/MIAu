import pytest
from test_data.user_creds import UserCredentials
from loguru import logger


@pytest.mark.regression
@pytest.mark.ui
def test_expected_elements_present(driver, login_page):
    # Navigate to the Contact Details page
    contact_list_page = login_page.complete_login(
        UserCredentials.it_email,
        UserCredentials.it_password
    )
    contact_details_page = contact_list_page.navigate_to_contact_details_page()
    contact_details_page.is_contact_details_page()

    # Checking page elements
    assert contact_details_page.is_text_correct(
        contact_details_page.elements['title'], 'Contact Details')

    for label, locator in contact_details_page.elements.items():
        if label == 'title':
            continue
        assert contact_details_page.is_element_present(locator), \
            "Expected element is not present on the Edit Contact page."
    logger.success(
        "The expected elements are present on the Edit Contact page"
    )
