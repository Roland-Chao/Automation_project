import pytest, requests, os, json
from page_objects.database_utils import DatabaseUtils
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def session():
    session = requests.Session()
    yield session
    session.close()

@pytest.fixture(scope="session")
def database():
    database = DatabaseUtils()
    yield database
    database.exit_sql()

@pytest.fixture
def login_info(worker_id):
    if worker_id == 'master' or worker_id == 'gw0':
        info = json.loads(os.getenv("ACCOUNT_1"))
    elif worker_id == 'gw1':
        info = json.loads(os.getenv("ACCOUNT_2"))
    elif worker_id == 'gw2':
        info = json.loads(os.getenv("ACCOUNT_3"))
    elif worker_id == 'gw3':
        info = json.loads(os.getenv("ACCOUNT_4"))
    elif worker_id == 'gw4':
        info = json.loads(os.getenv("ACCOUNT_5"))
    return info

@pytest.fixture
def browser():
    opt = Options()
    opt.add_argument("--window-size=1920,1080")
    opt.add_argument("--headless")
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opt)
    browser.maximize_window()
    yield browser
    browser.quit()