import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from page_objects.action_utils import ActionUtils

class ProductPage(ActionUtils):

    # 商品的第二個顏色(全商品共用)
    product_color = (By.XPATH, '//div[@class="product__color-selector"]/child::*')
    # 商品的第二個尺寸(全商品共用)
    product_size = (By.XPATH, '//div[@class="product__size-selector"]/child::*')
    # + btn
    quantity_add = (By.CLASS_NAME, 'product__quantity-add')
    # - btn
    quantity_minus = (By.CLASS_NAME, 'product__quantity-minus')
    # 商品總數
    quantity_value = (By.CLASS_NAME, 'product__quantity-value')
    # 加入購物車btn
    add_to_cart = (By.CLASS_NAME, 'product__add-to-cart-button')
    # 購物車icon
    icon_link = (By.CLASS_NAME, 'header__link-icon-cart')
    # 購物車icon總數
    icon_total = (By.CLASS_NAME, 'header__link-icon-cart-number')
    # 商品名稱
    product_title = (By.CLASS_NAME, 'product__title')
    # 商品id
    product_id = (By.CLASS_NAME, 'product__id')
    # 商品價錢
    product_price = (By.CLASS_NAME, 'product__price')
    # 結帳btn
    checkout_button = (By.CLASS_NAME, 'checkout-button')
    
    def __init__(self, set_browser):
        super().__init__(set_browser)
    
    def add_to_cart_btn(self):
        return self.find_element(self.add_to_cart)
    
    def icon_total_link(self):
        return self.find_element(self.icon_link)
    
    def icon_total_number(self):
        return self.find_element(self.icon_total)
    
    def select_color(self):
        color = random.choice(self.find_elements(self.product_color))
        color.click()
        return color
    
    def select_size(self):
        size = random.choice(self.find_elements(self.product_size))
        size.click()
        return size
        
    def click_increase_or_decrease_product(self, type, amount):
        for i in range(amount):
            if type == "increase":
                self.find_element(self.quantity_add).click()
            elif type == "decrease":
                self.find_element(self.quantity_minus).click()

    def total_number(self):
        return self.find_element(self.quantity_value)
    
    def get_product_title(self):
        return self.find_element(self.product_title)
    
    def get_product_id(self):
        return self.find_element(self.product_id)
    
    def get_product_price(self):
        return self.find_element(self.product_price)
    
    def check_out(self):
        return self.find_element(self.checkout_button)
    
    def convert_color(self, elem):
        result = elem.get_attribute("data_id").replace('color_code_', "")
        colors = {
            "FFFFFF": "白色",
            "FFDDDD": "粉紅",
            "CCCCCC": "淺灰",
            "DDFFBB": "亮綠",
            "BB7744": "淺棕",
            "DDF0FF": "淺藍",
        }
        return colors[result]