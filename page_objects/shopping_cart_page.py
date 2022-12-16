from selenium.webdriver.common.by import By
from page_objects.action_utils import ActionUtils
from selenium.webdriver.support.ui import Select
from enum import Enum
import time

class ShoppingCartPage(ActionUtils):
    # 商品名稱
    item_name = (By.CLASS_NAME, 'cart__item-name')
    # 商品id
    item_id = (By.CLASS_NAME, 'cart__item-id')
    # 商品顏色
    item_color = (By.CLASS_NAME, 'cart__item-color')
    # 商品size
    item_size = (By.CLASS_NAME, 'cart__item-size')
    # 商品單價
    item_price = (By.CLASS_NAME, 'cart__item-price-content')
    # 商品總價
    item_subtotal = (By.CLASS_NAME, 'cart__item-subtotal-content')
    # 購物車清單
    cart_item = (By.CLASS_NAME, 'cart__item')
    # 數量下拉選單
    quantity_selector = (By.CLASS_NAME ,'cart__item-quantity-selector')
    # 結帳完成頁 - 商品數量
    quantity_amount = (By.XPATH ,'//div[2][@class="cart__item-quantity"]/div[2]')
    # 刪除商品btn
    delete_btn = (By.CLASS_NAME, 'cart__delete-button')
    # 收件人姓名
    receiver_name = (By.XPATH, '//div[text()="收件人姓名"]/following-sibling::input')
    # 收件人Email
    receiver_email = (By.XPATH, '//div[text()="Email"]/following-sibling::input')
    # 收件人手機
    receiver_mobile = (By.XPATH, '//div[text()="手機"]/following-sibling::input')
    # 收件人地址
    receiver_address = (By.XPATH, '//div[text()="地址"]/following-sibling::input')
    # 配送時間
    deliver_time = (By.CSS_SELECTOR, 'input[type="radio"]')
    # 信用卡欄位 - 信用卡號
    card_number_iframe = (By.XPATH, '//*[@id="card-number"]/iframe')
    card_number = (By.XPATH, '//*[@id="cc-number"]')
    # 信用卡欄位 - 效期
    card_date_iframe = (By.XPATH, '//*[@id="card-expiration-date"]/iframe')
    card_date = (By.XPATH, '//*[@id="cc-exp"]')
    # 信用卡欄位 - 驗證碼
    card_ccv_iframe = (By.XPATH, '//*[@id="card-ccv"]/iframe')
    card_ccv = (By.XPATH, '//*[@id="cc-ccv"]')
    
    def __init__(self, set_browser):
        super().__init__(set_browser)
    
    def get_checkout_info(self, type=None):
        #考量有多個商品，商品以dict形式存放，以list回傳
        #商品資訊清單
        result = []
        # 取得商品總數
        list = len(self.find_elements(self.cart_item))
        for i in range(list):
            if type == "finish_page":
                amount = self.find_elements(self.quantity_amount)[i]
            else:
                amount = Select(self.find_elements(self.quantity_selector)[i]).first_selected_option   
            info = {}
            info["title"] = self.find_elements(self.item_name)[i].text
            info["id"] = self.find_elements(self.item_id)[i].text
            info["color"] = self.find_elements(self.item_color)[i].text
            info["size"] = self.find_elements(self.item_size)[i].text
            info["amount"] = amount.text
            info["price"] = self.find_elements(self.item_price)[i].text.replace("NT.", "")
            info["sub_total"] = self.find_elements(self.item_subtotal)[i].text.replace("NT.", "")
            #把商品資訊加到清單
            result.append(info)
        return result
    
    def edit_quantity(self, value):
        select = Select(self.find_element(self.quantity_selector))
        select.select_by_visible_text(value)
        return select
        
    def delete_item(self):
        # 按鈕可能為多個，用elements，取得list回來
        self.find_elements(self.delete_btn)[0].click()
        
    def get_subtotal(self):
        return self.find_element(self.item_subtotal).text.replace("NT.", "")
    
    def get_item_price(self):
        return self.find_element(self.item_price).text.replace("NT.", "")
    
    def select_deliver_time(self, option):
        class DeliverTime(Enum):
            Morning    = 0
            Afternoon  = 1
            Anytime    = 2

        if option != "":
            return self.find_elements(self.deliver_time)[DeliverTime[option].value].click()
    
    def filling_receiver_data(self, data):
        # 收件人資訊
        self.find_clickable_element(self.receiver_name).send_keys(data["Receiver"])
        self.find_clickable_element(self.receiver_email).send_keys(data["Email"])
        self.find_clickable_element(self.receiver_mobile).send_keys(data["Mobile"])
        self.find_clickable_element(self.receiver_address).send_keys(data["Address"])
        # 收件人時間
        self.select_deliver_time(data["Deliver Time"])
        # 填寫信用卡資訊
        self.switch_to_iframe(self.find_clickable_element(self.card_number_iframe))
        self.find_clickable_element(self.card_number).send_keys(data["Credit Card No"])
        self.switch_to_default_content()
        
        self.switch_to_iframe(self.find_clickable_element(self.card_date_iframe))
        self.find_clickable_element(self.card_date).send_keys(data["Expiry Date"])
        self.switch_to_default_content()
        
        self.switch_to_iframe(self.find_clickable_element(self.card_ccv_iframe))
        self.find_clickable_element(self.card_ccv).send_keys(data["Security Code"])
        self.switch_to_default_content()