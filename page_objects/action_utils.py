from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class ActionUtils:
    def __init__(self, browser):
        self.browser = browser
        self.browser_wait = WebDriverWait(browser, 10)
    
    def open_url(self, url):
        self.browser.get(url)
    
    def refresh_page(self):
        self.browser.refresh()
    
    def find_element(self, locator):
        return self.browser_wait.until(EC.presence_of_element_located((locator)))

    def find_elements(self, locator):
        return self.browser_wait.until(EC.presence_of_all_elements_located((locator)))
    
    def find_clickable_element(self, locator):
        return self.browser_wait.until(EC.element_to_be_clickable((locator)))
    
    def invisibility_of_element(self, locator):
        return self.browser_wait.until(EC.invisibility_of_element_located((locator)))
    
    def get_alert(self):
        return self.browser_wait.until(EC.alert_is_present())
    
    def get_localstorage(self, item):
        return self.browser.execute_script(f'return localStorage.getItem("{item}");')
    
    def set_localstorage(self, item, value):
        return self.browser.execute_script(f'localStorage.setItem("{item}", "{value}");')
    
    def switch_to_iframe(self, elem):
        self.browser.switch_to.frame(elem)

    def switch_to_default_content(self):
        self.browser.switch_to.default_content()
    
    def switch_to_window(self, tab_num):
        self.browser.switch_to.window(self.browser.window_handles[tab_num])
    
    def scroll_page_to_buttom(self):
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        while True:
            #滾動到最底
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #等待頁面loading
            time.sleep(2)
            #取得更新後的高度
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height