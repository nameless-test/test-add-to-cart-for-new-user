import pytest


@pytest.fixture(scope="session")
def browser_launch(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.close()
    context.close()
    browser.close()