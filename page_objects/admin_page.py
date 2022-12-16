import random
from selenium.webdriver.common.by import By
from page_objects.action_utils import ActionUtils
from selenium.webdriver.support.ui import Select
import os

class AdminPage(ActionUtils):

    # 新增商品按鈕
    create_new_product_btn = (By.XPATH, '//*[text()="Create New Product"]')
    # 商品類別
    product_category = (By.NAME, 'category')
    # 商品標題
    product_title_input = (By.NAME, 'title')
    # 商品敘述
    product_description_input = (By.NAME, 'description')
    # 商品價錢
    product_price_input = (By.NAME, 'price')
    # 商品備註
    product_texture_input = (By.NAME, 'texture')
    # 商品敘述
    product_wash_input = (By.NAME, 'wash')
    # 商品敘述
    product_place_input = (By.NAME, 'place')
    # 商品敘述
    product_note_input = (By.NAME, 'note')
    # 商品顏色
    product_color_checkbox = (By.ID, 'color_ids')
    # 商品尺寸
    product_size_checkbox = (By.NAME, 'sizes')
    # story
    product_story_input = (By.NAME, 'story')
    # main_image
    product_main_image = (By.NAME, 'main_image')
    # others_image
    product_others_image = (By.NAME, 'other_images')
    # 商品清單標題、id
    product_list_title = (By.ID, 'product_title')
    product_list_id = (By.ID, 'product_id')
    # 新增完成btn
    create_finish_btn = (By.XPATH, '//input[@value="Create"]')
    
    def __init__(self, set_browser):
        super().__init__(set_browser)
    
    def go_to_create_product_page(self):
        return self.find_element(self.create_new_product_btn).click()
    
    def select_product_category(self, value):
        category = Select(self.find_element(self.product_category))
        return category.select_by_visible_text(value)
    
    def select_product_color(self, data):
        colors_options = {
            "白色": 0,
            "亮綠": 1,
            "淺灰": 2,
            "淺棕": 3,
            "淺藍": 4,
            "深藍": 5,
            "粉紅": 6,
        }
        checkbox = self.find_elements(self.product_color_checkbox)
        if data == "全選":
            for i in range(len(checkbox)):
                checkbox[i].click()
        elif data != "":
            # 原始資料為 "白色, 亮綠"，以spilt切割組成list
            data = data.split(', ')
            for color in data:
                checkbox[colors_options[color]].click()
    
    def select_product_size(self, data):
        sizes_options = {
            "S": 0,
            "M": 1,
            "L": 2,
            "XL": 3,
            "F": 4,
        }
        checkbox = self.find_elements(self.product_size_checkbox)        
        if data == "全選":
            for i in range(len(checkbox)):
                checkbox[i].click()
        elif data != "":
            # 原始資料為 "L, XL"，以spilt切割組成list
            data = data.split(', ')
            for size in data:
                checkbox[sizes_options[size]].click()
    
    def delete_product(self, name):
        delete_btn = (By.XPATH, f'//td[text()="{name}"]/following-sibling::td/child::button')
        self.find_element(delete_btn).click()
    
    def find_product_by_title(self):
        result = []
        title = self.find_elements(self.product_list_title)
        for i in title:
            result.append(i.text)
        return result
    
    def create_new_product(self, data):
        # 商品圖片路徑
        picture1 = os.path.abspath('test_data/mainImage.jpg')
        picture2 = os.path.abspath('test_data/otherImage0.jpg')
        picture3 = os.path.abspath('test_data/otherImage1.jpg')
        
        # 選擇商品類別
        self.select_product_category(data["Category"])
        
        # 填寫商品資訊
        self.find_element(self.product_title_input).send_keys(data["Title"])
        self.find_element(self.product_description_input).send_keys(data["Description"])
        self.find_element(self.product_price_input).send_keys(data["Price"])
        self.find_element(self.product_texture_input).send_keys(data["Texture"])
        self.find_element(self.product_wash_input).send_keys(data["Wash"])
        self.find_element(self.product_place_input).send_keys(data["Place of Product"])
        self.find_element(self.product_note_input).send_keys(data["Note"])
        self.find_element(self.product_story_input).send_keys(data["Story"])
        
        # 填寫商品 顏色、尺寸
        self.select_product_color(data["Colors"])
        self.select_product_size(data["Sizes"])
        
        # 上傳圖片
        if data["Main Image"] == "sample image":
            self.find_element(self.product_main_image).send_keys(picture1)
            
        if data["Other Image 1"] == "sample image":
            self.find_elements(self.product_others_image)[0].send_keys(picture2)
            
        if data["Other Image 2"] == "sample image":
            self.find_elements(self.product_others_image)[1].send_keys(picture3)

        # 點選新增完成
        self.find_element(self.create_finish_btn).click()