# -*- coding: utf-8 -*-
import unittest

import time
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import *


class Cart(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost/litecart")

    def test_cart(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#box-most-popular")))

        quantity_cart = int(self.driver.find_element(By.CSS_SELECTOR, "#cart .quantity").text)

        while quantity_cart < 3:
            list_products = self.driver.find_elements(By.CSS_SELECTOR, "#box-most-popular li")

            first_product = list_products[0]
            first_product.click()

            quantity_cart = int(self.driver.find_element(By.CSS_SELECTOR, "#cart .quantity").text)

            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#box-product .information")))

            list_order_trs = self.driver.find_elements(By.CSS_SELECTOR, ".buy_now tr")
            if(len(list_order_trs) > 1):
                select = list_order_trs[0].find_element(By.CSS_SELECTOR, "[name*='options[Size]']")
                self.driver.execute_script("arguments[0].selectedIndex = 1; arguments[0].dispatchEvent(new Event('change'))", select)

            button_add_cart = self.driver.find_element(By.CSS_SELECTOR, ".buy_now [name='add_cart_product']")
            button_add_cart.click()

            new_quantity_cart = str(quantity_cart + 1)

            WebDriverWait(self.driver, 5).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#cart .quantity"), new_quantity_cart))

            quantity_cart = int(self.driver.find_element(By.CSS_SELECTOR, "#cart .quantity").text)

            logo = self.driver.find_element(By.CSS_SELECTOR, "#logotype-wrapper")
            logo.click()

        link_cart = self.driver.find_element(By.CSS_SELECTOR, "#cart .link[href*='checkout']")
        link_cart.click()

        # Кликаем в первую превьюшку, чтобы остановить вращение карусели с товарами
        list_preview_product = self.driver.find_elements(By.CSS_SELECTOR, ".shortcuts .shortcut")
        list_preview_product[0].click()

        items = self.driver.find_elements(By.CSS_SELECTOR, "#box-checkout-cart .viewport .items li")

        while len(items) != 0:
            table_order_summary = self.driver.find_element(By.CSS_SELECTOR, ".dataTable.rounded-corners")

            name_product_delete = items[0].find_element(By.CSS_SELECTOR, "a strong").text

            remove_button = items[0].find_element(By.CSS_SELECTOR, "[name='remove_cart_item']")
            remove_button.click()

            WebDriverWait(self.driver, 10).until(EC.staleness_of(table_order_summary))

            table_order_summary_items = self.driver.find_elements(By.CSS_SELECTOR, ".dataTable.rounded-corners tr:not(.header) .item")
            item_still_exists = False
            for i in range(len(table_order_summary_items)):
                if table_order_summary_items[i].text == name_product_delete:
                    item_still_exists = True
                    break
            assert not item_still_exists, "Элемент после удаления остался в таблице"

            items = self.driver.find_elements(By.CSS_SELECTOR, "#box-checkout-cart .viewport .items li")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
