import allure, pytest,os
from dotenv import load_dotenv
from page_objects.home_page import HomePage

class TestSearchProduct:
    load_dotenv()
    url = f'{os.getenv("DOMAIN")}/index.html'
    
    def test_search_by_keyword(self, browser):
        home = HomePage(browser)
        keyword = "洋裝"
        with allure.step('開啟商品網站'):
            browser.get(self.url)
        
        with allure.step(f'輸入 keyword:{keyword}'):
            home.search_product_by_keyword(keyword)
            
        with allure.step(f'驗證搜尋結果'):
            for title in home.search_result():
                assert keyword in title.text, f"The product name is {title.text}, not {keyword}"
                
    def test_search_without_keyword(self, browser):
        home = HomePage(browser)
        keyword = " "
        
        with allure.step('開啟商品網站'):
            browser.get(self.url)
            
        with allure.step(f'輸入 keyword:{keyword}'):
            home.search_product_by_keyword(keyword)
            
        with allure.step(f'驗證搜尋結果'):
            # 商品共有15件，比對scroll完成的數量
            assert len(home.search_result()) == 15, f"{len(home.search_result())}"

    def test_search_no_product_found(self, browser):
        home = HomePage(browser)
        keyword = "Hello"
        
        with allure.step('開啟商品網站'):
            browser.get(self.url)
            
        with allure.step(f'輸入 keyword:{keyword}'):
            home.search_product_by_keyword(keyword)
            
        with allure.step(f'驗證搜尋結果'):
            # invisibility_of_element 回傳True / False
            assert home.search_result("empty") == True, f'{home.search_result("empty")}'