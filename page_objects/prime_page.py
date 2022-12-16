import os, time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from page_objects.action_utils import ActionUtils

class PrimePage(ActionUtils):
    
    page_url = f'{os.getenv("DOMAIN")}/get_prime.html'
    # 信用卡欄位 - 信用卡號
    card_number_iframe = (By.XPATH, '//*[@id="card-number"]/iframe')
    card_number = (By.ID, "cc-number")
    # 信用卡欄位 - 效期
    card_date_iframe = (By.XPATH, '//*[@id="card-expiration-date"]/iframe')
    card_date = (By.ID, 'cc-exp')
    # 信用卡欄位 - 驗證碼
    card_ccv_iframe = (By.XPATH, '//*[@id="card-ccv"]/iframe')
    card_ccv = (By.ID, 'cc-cvc')
    # get_prime_btn
    get_prime_btn = (By.ID, 'checkoutBtn')
    
    def __init__(self, browser):
        super().__init__(browser)
        
    def get_prime_key(self):
        self.browser.get(self.page_url)
        # 填寫信用卡資訊 - 信用卡號
        self.switch_to_iframe(self.find_clickable_element(self.card_number_iframe))
        self.find_clickable_element(self.card_number).send_keys("4242-4242-4242-4242")
        self.switch_to_default_content()
        # 填寫信用卡資訊 - 效期
        self.switch_to_iframe(self.find_clickable_element(self.card_date_iframe))
        self.find_clickable_element(self.card_date).send_keys("1223")
        self.switch_to_default_content()
        # 填寫信用卡資訊 - 驗證碼
        self.switch_to_iframe(self.find_clickable_element(self.card_ccv_iframe))
        self.find_clickable_element(self.card_ccv).send_keys("123")
        self.switch_to_default_content()
        # 取得prime
        self.find_element(self.get_prime_btn).click()
        prime_key = self.get_alert().text
        self.get_alert().accept()
        
        return prime_key