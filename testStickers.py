# -*- coding: utf-8 -*-
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Stickers(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

        try:
            self.driver.get("http://localhost/litecart/en/")

        except:
            pass

    def test_stickers(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".content")))


        list_products = self.driver.find_elements(By.CSS_SELECTOR, ".product.column")

        failure_list = []

        for i in range(0, len(list_products)):
            sticker = (list_products[i].find_elements(By.CSS_SELECTOR, "[class*='sticker']"))


            if(len(sticker) != 1):
                name_product = list_products[i].find_element(By.CSS_SELECTOR, ".name").text
                failure_list.append(name_product)


        if(len(failure_list) != 0):
            error_message = "\nThere are some products with 0 or more than 1 sticker:"

            for i in range(0, len(failure_list)):
                error_message += "\n" + failure_list[i]

        assert len(failure_list) == 0, error_message



    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()