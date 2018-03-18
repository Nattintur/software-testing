# -*- coding: utf-8 -*-
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SignInAdmin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        try:
            self.driver.get("http://localhost/litecart/admin")
        except:
            pass

    def test_sign_in_admin(self):

        WebDriverWait(self.driver, 10).until(EC.title_is("My Store"))

        try:
            login = self.driver.find_element(By.NAME, 'username')
            login.send_keys("admin")
        except NoSuchElementException:
            print(u"Элемент не найден!")

        try:
            password = self.driver.find_element(By.NAME, 'password')
            password.send_keys("admin")
        except NoSuchElementException:
            print(u"Элемент не найден!")

        try:
            checkbox = self.driver.find_element(By.NAME, 'remember_me')
            checkbox.click()
        except NoSuchElementException:
            print(u"Элемент не найден!")

        try:
            button = self.driver.find_element(By.NAME, 'login')
            button.click()
        except NoSuchElementException:
            print(u"Элемент не найден!")

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='fa-sign-out']")))

        # sign_out = self.driver.find_element(By.CSS_SELECTOR, "[class*='fa-sign-out']")
        # sign_out.click()

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
