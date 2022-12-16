# Week 9 Part 2 (Deadline: 2022/12/18 23:59)

## [安裝相關說明]
    pip install -r requirements.txt

## [運行指令]
    //執行 shell 檔 (預設為五個 worker)
    sh script.sh ${要執行的測項}

    ex: sh script.sh test_XXX

## [專案結構說明]
    └── Automation_project
    │   │
    │   ├── allure_report // 放置測試報告
    │   │ 
    │   ├── api_objects // 放置 API 的 CLASS
    │   │   └── api_utils.py // 放置API共用的method
    │   │   └── A_api.py 
    │   │   └── B_api.py
    │   │ 
    │   ├── page_objects // 放置 web 頁面的CLASS
    │   │   └── action_utils.py // 放置web頁面共用的method
    │   │   └── XXX_page.py
    │   │   └── XXX_page.py
    │   │ 
    │   ├── test_data // 放置測試資料
    │   │   ├── get_data_from_excel // 處理 excel 的共用 method
    │   │   └── Stylish-Test Case.xlsx
    │   │   └── image1
    │   │   └── image2
    │   │ 
    │   ├── tests_web
    │   │   └── conftest.py // web 測試共用的 method
    │   │   └── test_webA.py
    │   │   └── test_webB.py
    │   │ 
    │   ├── tests_api
    │   │   └── conftest.py // api 測試共用的 method
    │   │   └── test_apiA.py
    │   │   └── test_apiB.py
    │   │ 
    │   ├── script.sh  // local 執行檔
    │   ├── jenkins.sh // jenkins 執行檔
    │   ├── pytest.ini // 設定 pytest 參數
    │   ├── requirements.txt // 套件管理檔
    └── └── .env // 管理環境參數(Domain、登入帳號)

## [驗證項目]
    UI: 驗證購物網站的UI流程
        1.登入
        2.搜尋商品
        3.搜尋商品
        4.加入購物車
        5.結帳
        6.後台商品管理

    API: 驗證購物網站API的正確、錯誤情境
        1.登入
        2.搜尋商品
        3.搜尋商品
        4.加入購物車
        5.結帳
        6.後台商品管理

## [.env 參數設定]
    DB_CONNECTION = '{
        "host": "*******",
        "database": "*******",
        "user": "*******",
        password='*******'
    }'

    // ACCOUNT 需要設定五個 ACCOUNT_1 - ACCOUNT_5
    ACCOUNT_1 = '{
        "account": "*******＠gmail.com",
        "password": "*******"
    }'