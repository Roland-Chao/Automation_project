from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from page_objects.action_utils import ActionUtils

class HomePage(ActionUtils):
    
    page_url = "http://54.201.140.239/index.html"
    search_input = (By.CLASS_NAME, "header__search-input")
    product_title = (By.CLASS_NAME, "product__title")
    category_woman = (By.LINK_TEXT, "女裝")
    category_man = (By.LINK_TEXT, "男裝")
    category_accessories = (By.LINK_TEXT, "配件")
    
    def __init__(self, set_browser):
        super().__init__(set_browser)
        
    def search_product_by_keyword(self, keyword):
        print(f"輸入:{keyword}")
        self.find_element(self.search_input).send_keys(keyword)
        print("按下Entern搜尋")
        self.find_element(self.search_input).send_keys(Keys.ENTER)

    def select_category(self, category):
        if category == "woman":
            return self.find_element(self.category_woman)
        elif category == "man":
            return self.find_element(self.category_man)
        elif category == "accessories":  
            return self.find_element(self.category_accessories)

    def search_result(self, type=None):
        if type == "empty":
            return self.invisibility_of_element(self.product_title)
        else:
            self.scroll_page_to_buttom()
            return self.find_elements(self.product_title)

    def assert_search_result(self, verify_item):
        assert len(self.search_result()) == len(verify_item)
        for i, element in enumerate(self.search_result()):
            assert element.text == verify_item[i], f'{element.text} is not in category' 