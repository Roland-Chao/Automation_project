import allure, pytest ,os
from dotenv import load_dotenv
from page_objects.product_page import ProductPage
from page_objects.action_utils import ActionUtils
from page_objects.shopping_cart_page import ShoppingCartPage

class TestShoppingCart:
    load_dotenv()
    url = os.getenv("DOMAIN")
    
    def test_shopping_cart_info_correct(self, browser):
        browser_action = ActionUtils(browser)
        product = ProductPage(browser)
        cart = ShoppingCartPage(browser)
        
        with allure.step('前往商品頁'):
            # 前開衩扭結洋裝
            browser.get(f'{self.url}/product.html?id=201807201824')
        
        with allure.step('選擇顏色、尺寸'):
            color = product.select_color()
            size = product.select_size()
            #組成商品資訊
            product_info = [{
                "title": product.get_product_title().text,
                "id": product.get_product_id().text,
                "color": f'顏色｜{product.convert_color(color)}',
                "size": f'尺寸｜{size.text}',
                "amount": product.total_number().text,
                "price": product.get_product_price().text.replace("TWD.", ""),
                "sub_total": str(int(product.total_number().text) * int(product.get_product_price().text.replace("TWD.", "")))
            },]
        
        with allure.step('點擊加入購物車 btn'): 
            product.add_to_cart_btn().click()

        with allure.step('切到 alert 彈窗'):
            browser_action.get_alert()
        
        with allure.step('驗證 alert 文案'):
            assert browser_action.get_alert().text == "已加入購物車", f"Error the text is {browser_action.get_alert().text}"
        
        with allure.step('pop 彈窗點選確定'):
            browser_action.get_alert().accept()
            
        with allure.step('點選購物車 icon'):
            product.icon_total_link().click()
            
        with allure.step('點選購物車 icon_num'):
             assert product.icon_total_number().text == "1", f'{product.icon_total_number().text}'
        
        with allure.step('驗證 url 是否為購物車頁面'):
            current_url = f'{self.url}/cart.html'
            assert browser.current_url == current_url, f'{browser.current_url}'
            
        with allure.step("確認購物清單商品資訊"):
            result = cart.get_checkout_info()
            for item in range(len(result)):
                for num in result[item]:
                    assert result[item][num] == product_info[item][num], f'{result[item][num]}'
                    
    def test_remove_product_from_cart(self, browser):
        browser_action = ActionUtils(browser)
        product = ProductPage(browser)
        cart = ShoppingCartPage(browser)
        product_id = ["201902191210", "201807242216"]
        product_list = []
        
        for i in range(len(product_id)):
            with allure.step(f'前往第 {i} 個商品頁'):
                browser.get(f'{self.url}/product.html?id={product_id[i]}')
            
            with allure.step(f'選擇:{product_id[i]} 顏色、尺寸'):
                color = product.select_color()
                size = product.select_size()
                
                #組成商品資訊
                product_info = {
                    "title": product.get_product_title().text,
                    "id": product.get_product_id().text,
                    "color": f'顏色｜{product.convert_color(color)}',
                    "size": f'尺寸｜{size.text}',
                    "amount": product.total_number().text,
                    "price": product.get_product_price().text.replace("TWD.", ""),
                    "sub_total": str(int(product.total_number().text) * int(product.get_product_price().text.replace("TWD.", "")))
                }
                product_list.append(product_info)
                
            with allure.step('點擊加入購物車 btn'): 
                product.add_to_cart_btn().click()

            with allure.step('切到 alert 彈窗'):
                browser_action.get_alert()
        
            with allure.step('驗證 alert 文案'):
                assert browser_action.get_alert().text == "已加入購物車", f"Error the text is {browser_action.get_alert().text}"
            
            with allure.step('pop 彈窗點選確定'):
                browser_action.get_alert().accept()
                
        with allure.step('點選購物車 icon'):
            product.icon_total_link().click()
            
        with allure.step('驗證購物車 icon_num'):
             assert product.icon_total_number().text == "2", f'{product.icon_total_number().text}'
        
        with allure.step('驗證 url 是否為購物車頁面'):
            current_url = f'{self.url}/cart.html'
            assert browser.current_url == current_url, f'{browser.current_url}'
        
        with allure.step('刪除一個商品'):
            # 刪除比對資料第一個商品
            del product_list[0]
            # 刪除購物車商品
            cart.delete_item()
        
        with allure.step('切到 alert 彈窗'):
            browser_action.get_alert()

        with allure.step('驗證 alert 文案'):
            assert browser_action.get_alert().text == "已刪除商品", f"Error the text is {browser_action.get_alert().text}"

        with allure.step('pop 彈窗點選確定'):
            browser_action.get_alert().accept()
                     
        with allure.step("驗證商品是否已被刪除"):
            result = cart.get_checkout_info()
            for item in range(len(result)):
                for num in result[item]:
                    assert result[item][num] == product_list[item][num], f'{result[item][num]}'

        with allure.step('驗證購物車 list 剩下一個商品'):
            result = cart.get_checkout_info()
            assert len(result) == 1, f'{len(result)}'
               
    def test_edit_quantity_in_cart(self, browser):
        browser_action = ActionUtils(browser)
        product = ProductPage(browser)
        cart = ShoppingCartPage(browser)
        
        with allure.step('前往商品頁'):
            browser.get(f'{self.url}/product.html?id=201807201824')
        
        with allure.step('選擇顏色、尺寸'):
            color = product.select_color()
            size = product.select_size()
            #組成商品資訊
            product_info = [{
                "title": product.get_product_title().text,
                "id": product.get_product_id().text,
                "color": f'顏色｜{product.convert_color(color)}',
                "size": f'尺寸｜{size.text}',
                "amount": product.total_number().text,
                "price": product.get_product_price().text.replace("TWD.", ""),
                "sub_total": str(int(product.total_number().text) * int(product.get_product_price().text.replace("TWD.", "")))
            },]
        
        with allure.step('點擊加入購物車 btn'): 
            product.add_to_cart_btn().click()

        with allure.step('切到 alert 彈窗'):
            browser_action.get_alert()
        
        with allure.step('驗證 alert 文案'):
            assert browser_action.get_alert().text == "已加入購物車", f"Error the text is {browser_action.get_alert().text}"
        
        with allure.step('pop 彈窗點選確定'):
            browser_action.get_alert().accept()
            
        with allure.step('點選購物車 icon'):
            product.icon_total_link().click()
            
        with allure.step('點選購物車 icon_num'):
             assert product.icon_total_number().text == "1", f'{product.icon_total_number().text}'
        
        with allure.step('驗證 url 是否為購物車頁面'):
            current_url = f'{self.url}/cart.html'
            assert browser.current_url == current_url, f'{browser.current_url}'
            
        with allure.step("確認購物清單商品資訊"):
            result = cart.get_checkout_info()
            for item in range(len(result)):
                for num in result[item]:
                    assert result[item][num] == product_info[item][num], f'{result[item][num]}'
                    
        with allure.step("修改商品數量"):
            value = cart.edit_quantity("9")
        
        with allure.step('切到 alert 彈窗'):
            browser_action.get_alert()

        with allure.step('驗證 alert 文案'):
            assert browser_action.get_alert().text == "已修改數量", f"Error the text is {browser_action.get_alert().text}"

        with allure.step('pop 彈窗點選確定'):
            browser_action.get_alert().accept()
            
        with allure.step("驗證修改商品數量"):
            assert value.first_selected_option.text == "9", f'{value.first_selected_option.text}'

        with allure.step("驗證商品金額是否正確"):
            total = int(cart.get_subtotal())
            item_price = int(cart.get_item_price())
            expect_total = item_price * 9
            assert (expect_total) == total, f'{expect_total}'