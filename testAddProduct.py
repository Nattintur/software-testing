# -*- coding: utf-8 -*-
import unittest

import os
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import *


def is_element_present(self, *args):
    try:
        self.driver.find_element(*args)
        return True
    except NoSuchElementException:
        return False

def sign_in(self, user, password_user):
    assert (is_element_present(self, By.NAME, 'username'))
    login = self.driver.find_element(By.NAME, 'username')
    login.send_keys(user)

    assert (is_element_present(self, By.NAME, 'password'))
    password = self.driver.find_element(By.NAME, 'password')
    password.send_keys(password_user)

    assert (is_element_present(self, By.NAME, 'remember_me'))
    checkbox = self.driver.find_element(By.NAME, 'remember_me')
    checkbox.click()

    assert (is_element_present(self, By.NAME, 'login'))
    button = self.driver.find_element(By.NAME, 'login')
    button.click()

class AddProduct(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost/litecart/admin")

        sign_in(self, "admin", "admin")

    def test_add_product(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#sidebar")))
        catalog = self.driver.find_element(By.CSS_SELECTOR, "#box-apps-menu a[href*='?app=catalog&doc=catalog']")
        catalog.click()

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
        button = self.driver.find_element(By.CSS_SELECTOR, "a[href*='category_id=0&app=catalog&doc=edit_product']")
        button.click()

        radio_buttons = self.driver.find_elements(By.CSS_SELECTOR, "#tab-general [name='status']")
        if not radio_buttons[0].get_attribute("checked"):
            radio_buttons[0].click()

        name = self.driver.find_element(By.CSS_SELECTOR, "[name='name[en]']")
        name.send_keys("Cat")

        code = self.driver.find_element(By.CSS_SELECTOR, "[name='code']")
        code.send_keys("0001")

        quantity = self.driver.find_element(By.CSS_SELECTOR, "[name='quantity']")
        quantity.clear()
        quantity.send_keys("1")

        file = self.driver.find_element(By.CSS_SELECTOR, "[name='new_images[]']")
        file.send_keys(os.path.abspath("cat.jpg"))

        date_valid_from = self.driver.find_element(By.CSS_SELECTOR, "[name='date_valid_from']")
        date_valid_from.send_keys("09/04/2018")

        date_valid_to = self.driver.find_element(By.CSS_SELECTOR, "[name='date_valid_to']")
        date_valid_to.send_keys("09/04/2018")

        tab_information = self.driver.find_element(By.CSS_SELECTOR, ".tabs [href*='#tab-information']")
        tab_information.click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tab-information")))

        manufacturer_id = self.driver.find_element(By.CSS_SELECTOR, "[name*='manufacturer_id']")
        self.driver.execute_script("arguments[0].selectedIndex = 1; arguments[0].dispatchEvent(new Event('change'))", manufacturer_id)

        keywords = self.driver.find_element(By.CSS_SELECTOR, "[name='keywords']")
        keywords.send_keys("cat")

        short_description = self.driver.find_element(By.CSS_SELECTOR, "[name*='short_description[en]']")
        short_description.send_keys("CT")

        descr = self.driver.find_element(By.CSS_SELECTOR, ".trumbowyg-editor")
        descr.send_keys("description")

        tab_price = self.driver.find_element(By.CSS_SELECTOR, ".tabs [href*='#tab-prices']")
        tab_price.click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tab-prices")))

        purchase_price = self.driver.find_element(By.CSS_SELECTOR, "[name='purchase_price']")
        purchase_price.clear()
        purchase_price.send_keys("10.000")

        prices_USD = self.driver.find_element(By.CSS_SELECTOR, "[name='prices[USD]']")
        prices_USD.send_keys("10.000")

        button_save = self.driver.find_element(By.CSS_SELECTOR, ".button-set [name='save']")
        button_save.click()

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dataTable")))
        last_tr = self.driver.find_elements(By.CSS_SELECTOR, ".dataTable .row")
        product_name = last_tr[2].find_element(By.CSS_SELECTOR, "a").text

        assert str(product_name) == "Cat"

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()