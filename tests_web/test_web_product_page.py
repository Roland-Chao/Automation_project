import allure, pytest,os
from dotenv import load_dotenv
from page_objects.product_page import ProductPage
from page_objects.action_utils import ActionUtils

class TestSearchProduct:
    load_dotenv()
    url = f'{os.getenv("DOMAIN")}/product.html?id=201807201824'
    
    @allure.title("商品color測項")
    def test_color_selection(self, browser):
        product = ProductPage(browser)
        
        with allure.step('開啟商品網站'):
            browser.get(self.url)
            
        with allure.step('選擇商品 color'):
            product.select_color()
            
        with allure.step('驗證顏色是否被選取'):
            result = product.select_color()
            assert "selected" in result.get_attribute("class"), f'highlighted Fail !!!'
            
    @allure.title("商品 size 驗證")
    def test_size_selection(self, browser):
        product = ProductPage(browser)
        
        with allure.step('開啟商品網站'):
            browser.get(self.url)
            
        with allure.step('選擇尺寸'):
            product.select_size()
            
        with allure.step('驗證尺寸是否被選取'):
            result = product.select_size()
            assert "selected" in result.get_attribute("class"), f'highlighted Fail !!!'
            
    @allure.title("新增商品驗證")
    def test_increase_quantity(self, browser):
        product = ProductPage(browser)
        
        with allure.step('開啟商品網站'):
            browser.get(self.url)
        
        with allure.step('選擇商品 size'):
            product.select_size().click()
        
        with allure.step('增加8個商品'):
            product.click_increase_or_decrease_product("increase", 8)
            result = product.total_number()
            assert result.text == "9", f"商品數量錯誤:{result.text}"
        
        with allure.step('再新增2個商品'):
            product.click_increase_or_decrease_product("increase", 2)
        
        with allure.step('驗證商品總數'):
            number = product.total_number()
            assert number.text == "9", f"商品數量錯誤:{number.text}"
        
    @allure.title("減少商品驗證")
    def test_decrease_quantity(self, browser):
        product = ProductPage(browser)
        
        with allure.step('開啟商品網站'):
            browser.get(self.url)
            
        with allure.step('選擇商品 size'):
            product.select_size().click()
            
        with allure.step('增加8個商品'):
            product.click_increase_or_decrease_product("increase", 8)
            number = product.total_number()
            assert number.text == "9", f"商品數量錯誤:{number.text}"
        
        with allure.step('減少8個商品'):
            product.click_increase_or_decrease_product("decrease", 8)
            assert number.text == "1", f"商品數量錯誤:{number.text}"
    
    @allure.title("加入購物車失敗驗證") 
    def test_add_to_cart_fail(self, browser):
        product = ProductPage(browser)
        browser_action = ActionUtils(browser)
        
        with allure.step('開啟商品網站'):
            browser.get(self.url)
            
        with allure.step('驗證 btn 文案'):
            assert product.add_to_cart_btn().text == "請選擇尺寸", f"Error the text is {product.add_to_cart_btn().text}"
            
        with allure.step('驗證加入購物車 btn 文案'):
            product.add_to_cart_btn().click()
        
        with allure.step('切到 alert 彈窗'):
            browser_action.get_alert()
        
        with allure.step('驗證 alert 文案'):
            assert browser_action.get_alert().text == "請選擇尺寸", f"Error the text is {browser_action.get_alert().text}"
        
        with allure.step('pop 彈窗點選確定'):
            browser_action.get_alert().accept()
        
    @allure.title("加入購物車成功驗證")
    def test_add_to_cart_success(self, browser):
        product = ProductPage(browser)
        browser_action = ActionUtils(browser)
        
        with allure.step('開啟商品網站'):
            browser.get(self.url)
            
        with allure.step('選擇商品 size'):
            product.select_size().click()
        
        with allure.step('驗證商品數為1個'):
            assert product.total_number().text == "1", f"商品數量錯誤:{product.total_number().text}"
            
        with allure.step('驗證加入購物車 btn 文案'):
            assert product.add_to_cart_btn().text == "加入購物車", f"Error the text is {product.add_to_cart_btn().text}"
            
        with allure.step('點擊加入購物車 btn'): 
            product.add_to_cart_btn().click()

        with allure.step('切到 alert 彈窗'):
            browser_action.get_alert()
        
        with allure.step('驗證 alert 文案'):
            assert browser_action.get_alert().text == "已加入購物車", f"Error the text is {browser_action.get_alert().text}"
        
        with allure.step('pop 彈窗點選確定'):
            browser_action.get_alert().accept()
        
        with allure.step('驗證購物車 icon 數量為1'):
            assert product.icon_total_number().text == "1", f"Error the text is {product.icon_total_number().text}"
            
    @allure.title("未選擇尺寸")
    
    def test_quantity_editor_disabled(self, browser):
        product = ProductPage(browser)
        browser_action = ActionUtils(browser)
        
        with allure.step('開啟商品網站'):
            browser.get(self.url)
        
        with allure.step('新增1個商品'):
            product.click_increase_or_decrease_product("increase", 1)
            result = product.total_number()
            assert result.text == "1", f"商品數量錯誤:{result}"
            
        with allure.step('驗證加入購物車 btn 文案'):
            assert product.add_to_cart_btn().text == "請選擇尺寸", f"Error the text is {product.add_to_cart_btn().text}"
            
        with allure.step('點擊加入購物車 btn'):
            product.add_to_cart_btn().click()
            
        with allure.step('切到 alert 彈窗'):
            browser_action.get_alert()
            
        with allure.step('驗證 alert 文案'):
            assert browser_action.get_alert().text == "請選擇尺寸", f"Error the text is {browser_action.get_alert().text}"
            
        with allure.step('pop 彈窗點選確定'):
            browser_action.get_alert().accept()