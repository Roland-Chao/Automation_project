import allure, os, pytest
from dotenv import load_dotenv
from page_objects.product_page import ProductPage
from page_objects.action_utils import ActionUtils
from page_objects.shopping_cart_page import ShoppingCartPage
from page_objects.login_page import LoginPage
from test_data.get_data_from_excel import GetDataFromExcel

class TestCheckOut:
    load_dotenv()
    url = os.getenv("DOMAIN")
    path = os.path.abspath("test_data/Stylish-Test Case.xlsx")
    data = GetDataFromExcel(path)
    
    def test_checkout_with_empty(self, browser, worker_id):
        browser_action = ActionUtils(browser)
        product_page = ProductPage(browser)
        login_page = LoginPage(browser)
        login_info = login_page.get_parallel_login_account(worker_id)
        
        with allure.step('前往登入頁'):
            # 前開衩扭結洋裝
            browser.get(f'{self.url}/login.html')
            
        with allure.step('會員登入'):
            login_page.stylish_login(login_info["account"], login_info["password"])
            
        with allure.step('驗證彈窗: Login Success'):
            alert = browser_action.get_alert()
            assert  alert.text == "Login Success", f'{alert.text}'
    
        with allure.step('關閉彈窗'):
            alert.accept()

        with allure.step('點擊購物車 icon'):
            product_page.icon_total_link().click()
   
        with allure.step('點擊確認付款'):
            product_page.check_out().click()
            
        with allure.step('驗證彈窗: 尚未選購商品'):
            alert = browser_action.get_alert()
            assert  alert.text == "尚未選購商品", f'{alert.text}'   
            
        with allure.step('關閉彈窗'):
            alert.accept()
                
    @pytest.mark.parametrize('test_data', data.create_test_data("Checkout with Invalid Value"))
    def test_checkout_with_invaild_values(self, browser, test_data, worker_id):
        browser_action = ActionUtils(browser)
        cart = ShoppingCartPage(browser)
        product_page = ProductPage(browser)
        login_page = LoginPage(browser)
        login_info = login_page.get_parallel_login_account(worker_id)
        
        with allure.step('前往登入頁'):
            browser.get(f'{self.url}/login.html')
            
        with allure.step('會員登入'):
            login_page.stylish_login(login_info["account"], login_info["password"])
            
        with allure.step('驗證登入成功'):
            alert = browser_action.get_alert()
            assert  alert.text == "Login Success", f'{alert.text}'
    
        with allure.step('關閉彈窗'):
            alert.accept()
            
        with allure.step('前往商品頁'):
            # 前開衩扭結洋裝
            browser.get(f'{self.url}/product.html?id=201807201824')
        
        with allure.step('將商品加入購物車'):
            product_page.select_color()
            product_page.select_size()
            product_page.add_to_cart_btn().click()
            browser_action.get_alert()
            assert browser_action.get_alert().text == "已加入購物車", f"Error the text is {browser_action.get_alert().text}"
            browser_action.get_alert().accept()
            
        with allure.step('前往購物車頁'):
            product_page.icon_total_link().click()
            
        with allure.step('填寫收件人資料'):
            cart.filling_receiver_data(test_data)
            product_page.check_out().click()
            
        with allure.step(f'驗證彈窗文案:{test_data["Alert Msg"]}'):
            alert = browser_action.get_alert()
            assert  alert.text == test_data["Alert Msg"], f'{alert.text}'
            alert.accept()
            
    @pytest.mark.parametrize('test_data', data.create_test_data("Checkout with Valid Value"))
    def test_checkout_with_valid_values(self, browser, test_data, worker_id):
        browser_action = ActionUtils(browser)
        cart = ShoppingCartPage(browser)
        product_page = ProductPage(browser)
        login_page = LoginPage(browser)
        login_info = login_page.get_parallel_login_account(worker_id)
        
        with allure.step('前往登入頁'):
            browser.get(f'{self.url}/login.html')
            
        with allure.step('會員登入'):
            login_page.stylish_login(login_info["account"], login_info["password"])
            
        with allure.step('驗證登入成功'):
            alert = browser_action.get_alert()
            assert  alert.text == "Login Success", f'{alert.text}'
    
        with allure.step('關閉彈窗'):
            alert.accept()
            
        with allure.step('前往商品頁'):
            # 前開衩扭結洋裝
            browser.get(f'{self.url}/product.html?id=201807201824')
        
        with allure.step('將商品加入購物車'):
            color = product_page.select_color()
            size = product_page.select_size()
            #組成商品資訊
            product_info = [{
                "title": product_page.get_product_title().text,
                "id": product_page.get_product_id().text,
                "color": f'顏色｜{product_page.convert_color(color)}',
                "size": f'尺寸｜{size.text}',
                "amount": product_page.total_number().text,
                "price": product_page.get_product_price().text.replace("TWD.", ""),
                "sub_total": str(int(product_page.total_number().text) * int(product_page.get_product_price().text.replace("TWD.", "")))
            },]
        
            product_page.add_to_cart_btn().click()
            browser_action.get_alert()
            assert browser_action.get_alert().text == "已加入購物車", f"Error the text is {browser_action.get_alert().text}"
            browser_action.get_alert().accept()
            
        with allure.step('前往購物車頁'):
            product_page.icon_total_link().click()

        with allure.step('填寫收件人資料'):
            cart.filling_receiver_data(test_data)
            product_page.check_out().click()
            
        with allure.step('驗證彈窗: 付款成功'):
            alert = browser_action.get_alert()
            assert  alert.text == "付款成功", f'{alert.text}'
            
        with allure.step('關閉彈窗'):
            alert.accept()

        with allure.step('結帳完成頁面：驗證商品資訊'):
            order_info = cart.get_checkout_info("finish_page")
            for item in range(len(order_info)):
                for num in order_info[item]:
                    assert order_info[item][num] == product_info[item][num], f'{order_info[item][num]}'