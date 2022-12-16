import os, requests
from api_objects.api_utils import APIUtils

class AdminProductAPI(APIUtils):  

    def __init__(self, session):
        super().__init__(session)
        self.session = session
        self.url = f'{os.getenv("DOMAIN")}/api/1.0/admin/product'
        self.form_data =  {
            'category': '',
            'title' : '',
            'description' : '',
            "price" : 0,
            'texture' : '',
            'wash' :  '',
            'place' :  '',
            'note' :  '',
            'color_ids' :  [],
            'sizes' :  [],
            'story' :  '' ,
        }
        self.files = []
        
    def set_from_file(self, data):
        self.request_files = self.files.copy()
        main_image = 'test_data/mainImage.jpg'
        other_image_1 = 'test_data/otherImage1.jpg'
        other_image_2 = 'test_data/otherImage1.jpg'
        
        # main_image
        if data["Main Image"] == "sample image":
            self.request_files.append(("main_image", open(main_image, "rb")))
        else:
            self.request_files.append(("main_image", None))
            
        # other_image1
        if data["Other Image 1"] == "sample image":
            self.request_files.append(("other_images", open(other_image_1, 'rb')))
        else:
            self.request_files.append(("other_images", None))
            
        # other_image2
        if data["Other Image 2"] == "sample image":
            self.request_files.append(("other_images", open(other_image_2, 'rb')))
        else:
            self.request_files.append(("other_images", None))
            
        return self.request_files
    
    def set_form_data(self, data):
        self.request_data = self.form_data.copy()
        # 組成 form_data
        self.request_data["category"] = data["Category"]
        self.request_data["title"] = data["Title"]
        self.request_data["description"] = data["Description"]
        self.request_data["price"] = data["Price"]
        self.request_data["texture"] = data["Texture"]
        self.request_data["wash"] = data["Wash"]
        self.request_data["place"] = data["Place of Product"]
        self.request_data["note"] = data["Note"]
        self.request_data["story"] = data["Story"]
        # 顏色
        colors = data["ColorIDs"].split(',')
        if colors != "":
            for color in colors:
                self.request_data["color_ids"].append(color)
        # 尺寸  
        sizes = data["Sizes"].split(',')
        if sizes != "":
            for size in sizes:
                self.request_data["sizes"].append(size)

        return self.request_data
        
    def send_request(self, **kwargs):
        self.response = self.post_request(**kwargs)
        return self.response