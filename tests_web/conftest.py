import pytest
import allure

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from allure_commons.types import AttachmentType
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def browser():
    opt = Options()
    opt.add_argument("--window-size=1920,1080")
    opt.add_argument("--headless")
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opt)
    browser.maximize_window()
    yield browser
    allure.attach(browser.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
    browser.quit()