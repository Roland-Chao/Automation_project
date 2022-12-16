import allure, pytest, os
from dotenv import load_dotenv
from page_objects.home_page import HomePage

class TestSearchCategory:
    load_dotenv()
    url = f'{os.getenv("DOMAIN")}/index.html'
    
    def test_category_woman(self, browser):
        home = HomePage(browser)
        
        with allure.step("開啟 STYLISH 首頁..."):
            browser.get(self.url)

        with allure.step("選擇 man 類別"):
            home.select_category("man").click()
            
        with allure.step("驗證結果"):
            home.search_result()
            category = ["純色輕薄百搭襯衫", "時尚輕鬆休閒西裝", "經典商務西裝"]
            assert len(home.search_result()) == len(category)
            for i, element in enumerate(home.search_result()):
                assert element.text == category[i], f'{element.text} is not in category' 
    
    def test_category_man(self, browser):
        home = HomePage(browser)
        
        with allure.step("開啟 STYLISH 首頁..."):
            browser.get(self.url)
            
        with allure.step("選擇 woman 類別"):
            home.select_category("woman").click()
            
        with allure.step("驗證結果"):
            home.search_result()
            category = ["前開衩扭結洋裝", "透肌澎澎防曬襯衫", "小扇紋細織上衣", 
                        "活力花紋長筒牛仔褲", "精緻扭結洋裝", "透肌澎澎薄紗襯衫",
                        "小扇紋質感上衣", "經典修身長筒牛仔褲"]
            assert len(home.search_result()) == len(category)
            for i, element in enumerate(home.search_result()):
                assert element.text == category[i], f'{element.text} is not in category'
                
    def test_category_accessories(self, browser):
        home = HomePage(browser)
        
        with allure.step("開啟 STYLISH 首頁..."):
            browser.get(self.url)
            
        with allure.step("選擇 accessories 類別"):
            home.select_category("accessories").click()
            home.search_result()
            category = ["夏日海灘戶外遮陽帽", "經典牛仔帽", "卡哇伊多功能隨身包", "柔軟氣質羊毛圍巾"]
        
        with allure.step("驗證結果"):
            assert len(home.search_result()) == len(category)
            for i, element in enumerate(home.search_result()):
                assert element.text == category[i], f'{element.text} is not in category'