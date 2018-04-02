# -*- coding: utf-8 -*-
import unittest

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

class Example(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        # self.driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver')

        ## версия FF должна быть 45, запуск по-старому, стабильная версия
        # self.driver = webdriver.Firefox(executable_path='/usr/bin/firefox', capabilities={"marionette":False})

        ## версия обновляется каждый вечер, девелоперская версия
        # self.driver = webdriver.Firefox(firefox_binary="/usr/bin/firefox-trunk")

        # Запуск по-новому версия, FF последней версии для gecodriver 0.20
        # self.driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver', capabilities={"marionette":True})



    def test_example(self):
        try:
            self.driver.get("https://www.yandex.ru")
        except:
            pass

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()