from selenium.webdriver.common.by import By
from page_objects.action_utils import ActionUtils
import json, os

class LoginPage(ActionUtils):

    email_input = (By.ID, 'email')
    password_input = (By.ID, 'pw')
    login_btn = (By.CLASS_NAME, 'login100-form-btn')
    logout_btn = (By.XPATH, '//div[@class="profile__content"]/button')
    
    def __init__(self, set_browser):
        super().__init__(set_browser)
        
    def stylish_login(self, email, password):
        self.find_element(self.email_input).send_keys(email)
        self.find_element(self.password_input).send_keys(password)
        self.find_element(self.login_btn).click()
        
    def stylish_logout(self):
        self.find_element(self.logout_btn).click()
        
    def get_parallel_login_account(self, worker_id):
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
        