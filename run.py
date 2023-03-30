import pytest
import os

if __name__ == '__main__':
    pytest.main(['-v', '--alluredir', './result', '--clean-alluredir'])
    os.system('allure generate ./result/ -o ./report_allure/ --clean')