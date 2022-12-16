echo "-------切換至虛擬環境-------"
python3 -m venv ~/my_virtual_env
source ~/my_virtual_env/bin/activate

echo "-------執行 $test_case 測試-------"
pytest -n 5 -k $test_case --alluredir "${WORKSPACE}/allure-results" --reruns 2