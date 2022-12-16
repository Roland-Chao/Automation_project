echo "執行${1}測試";
pytest -k ${1} -n 5 --alluredir=./allure_report --clean-alluredir
echo "打開allure報告";
allure serve ./allure_report