import allure, pytest ,time, os
from dotenv import load_dotenv
from page_objects.login_page import LoginPage
from page_objects.action_utils import ActionUtils

class TestWebLogin:
    load_dotenv()
    url = os.getenv("DOMAIN")

    def test_login_and_logout(self, browser, worker_id):
        login_page = LoginPage(browser)
        browser_action = ActionUtils(browser)
        login_info = login_page.get_parallel_login_account(worker_id)
        
        with allure.step("開啟 STYLISH 登入頁..."):
            browser.get(f'{self.url}/login.html')
            
        with allure.step("輸入帳密登入"): 
            login_page.stylish_login(login_info["account"], login_info["password"])
            time.sleep(1)
        
        with allure.step("驗證 alert 是否登入成功"): 
            browser_action.get_alert()
            print(browser_action.get_alert().text)
            assert browser_action.get_alert().text == "Login Success", f'browser_action.get_alert().text'
        
        with allure.step("關閉 alert 彈窗"):  
            browser_action.get_alert().accept()
            
        with allure.step("驗證 LocalStorage 有 Token"):
            token = browser_action.get_localstorage("jwtToken")
            assert token != None, f'Error !!! {token} is in localstorage'
            
        with allure.step("登出"):
            login_page.stylish_logout()
            time.sleep(1)
            
        with allure.step("驗證 alert 否登出成功"): 
            browser_action.get_alert()
            print(browser_action.get_alert().text)
            assert browser_action.get_alert().text == "Logout Success", f'browser_action.get_alert().text'
        
        with allure.step("關閉 alert 彈窗"): 
            browser_action.get_alert().accept()
            
        with allure.step("驗證 Token 是否被清除"): 
            token = browser_action.get_localstorage("jwtToken")
            assert token == None, f'Error !!! {token} is in localstorage'
          
    def test_login_with_incorrect_data(self, browser, worker_id):
        login_page = LoginPage(browser)
        browser_action = ActionUtils(browser)
        login_info = login_page.get_parallel_login_account(worker_id)
        password = "654321"
        
        with allure.step("開啟 STYLISH 登入頁..."):
            browser.get(f'{self.url}/login.html')
            
        with allure.step("輸入帳密登入"): 
            login_page.stylish_login(login_info["account"], password)
            time.sleep(1)
        
        with allure.step("驗證 alert 是否登入失敗"): 
            browser_action.get_alert()
            assert browser_action.get_alert().text == "Login Failed", f'{browser_action.get_alert().text}'
        
        with allure.step("關閉 alert 彈窗"):  
            browser_action.get_alert().accept()
            
        with allure.step("驗證 LocalStorage 沒有Token"):
            token = browser_action.get_localstorage("jwtToken")
            assert token == None, f'Error !!! {token} is in localstorage'
            
    def test_login_with_invalid_access_token(self, browser, worker_id):
        login_page = LoginPage(browser)
        browser_action = ActionUtils(browser)
        login_info = login_page.get_parallel_login_account(worker_id)
        
        with allure.step("開啟 STYLISH 登入頁..."):
            browser.get(f'{self.url}/login.html')
            
        with allure.step("輸入帳密登入"): 
            login_page.stylish_login(login_info["account"], login_info["password"])
            time.sleep(1)
        
        with allure.step("驗證 alert 是否登入成功"): 
            browser_action.get_alert()
            print(browser_action.get_alert().text)
            assert browser_action.get_alert().text == "Login Success", f'browser_action.get_alert().text'
        
        with allure.step("關閉 alert 彈窗"):  
            browser_action.get_alert().accept()
            
        with allure.step("驗證 LocalStorage 沒有 Token"):
            token = browser_action.get_localstorage("jwtToken")
            assert token != None, f'Error !!! {token} is in localstorage'
            
        with allure.step("登出"):
            login_page.stylish_logout()
            time.sleep(1)
            
        with allure.step("驗證 alert 否登出成功"): 
            browser_action.get_alert()
            print(browser_action.get_alert().text)
            assert browser_action.get_alert().text == "Logout Success", f'browser_action.get_alert().text'
        
        with allure.step("關閉 alert 彈窗"): 
            browser_action.get_alert().accept()
            
        with allure.step("將登入的 Toke 寫回 LocalStorage"):
            login_page.set_localstorage("jwtToken", token)

        with allure.step("前往 Profile 頁面"):
            browser.get(f'{self.url}/profile.html')
            time.sleep(1)
            
        with allure.step("驗證 alert 否登出成功"): 
            browser_action.get_alert()
            print(browser_action.get_alert().text)
            assert browser_action.get_alert().text == "Invalid Access Token", f'browser_action.get_alert().text'

        with allure.step("關閉 alert 彈窗"): 
            browser_action.get_alert().accept()
