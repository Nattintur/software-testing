# -*- coding: utf-8 -*-
import unittest

from selenium import webdriver

class Example(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_example(self):
        try:
            self.driver.get("https://www.yandex.ru")
        except:
            pass

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()