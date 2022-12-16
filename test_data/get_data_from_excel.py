from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

class GetDataFromExcel:
    def __init__(self, path):
        self.path = path
        
    def read_data(self, sheet_name):
        self.data = pd.read_excel(self.path, sheet_name = sheet_name, dtype=str)
        return self.data
    
    def create_test_data(self, sheet_name):
        self.test_data = self.read_data(sheet_name).fillna('').to_dict("records")
        for row_data in self.test_data:
            for value in row_data:
                if "chars" in row_data[value]: 
                    row_data[value] = int(row_data[value].replace("chars", "")) * "x"
            
        return self.test_data