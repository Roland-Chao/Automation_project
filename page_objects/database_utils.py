import mysql.connector, allure, os, json
from dotenv import load_dotenv

class DatabaseUtils:
    load_dotenv()
    db_info = json.loads(os.getenv("DB_CONNECTION")) 
    
    def __init__(self):
        with allure.step(f"連接 MYSQL DB"):
            self.connection = mysql.connector.connect(
                host = self.db_info["host"],
                port = int(self.db_info["port"]),
                user = self.db_info["user"],
                password = self.db_info["password"],)
            self.cursor = self.connection.cursor(dictionary=True)
            
    def execute_query(self, sql_string, query_data=None):
        with allure.step(f"query string: \n string: {sql_string}\n data: {query_data}"):
            self.cursor.execute(sql_string, query_data)

    def commit_query(self):
        self.connection.commit()
        
    def fetchall_result(self):
        with allure.step("取得資料庫全部搜尋結果"):
            return self.cursor.fetchall()
    
    def fetchone_result(self):
        with allure.step("取得資料庫一筆搜尋結果"):
            return self.cursor.fetchone()   
         
    def exit_sql(self):
        with allure.step("關閉資料庫"):
            self.cursor.close()
            self.connection.close()