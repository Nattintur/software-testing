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


def sign_in_online_store(self, email_, password_):
    email = self.driver.find_element(By.CSS_SELECTOR, "#box-account-login [name='email']")
    email.send_keys(email_)

    password = self.driver.find_element(By.CSS_SELECTOR, "#box-account-login [name='password']")
    password.send_keys(password_)

    button = self.driver.find_element(By.CSS_SELECTOR, "#box-account-login [name='login']")
    button.click()

class CheckIn(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost/litecart")

    def test_check_in_app(self):
        self.driver.find_element(By.CSS_SELECTOR, "[name='login_form'] a[href*='create_account']").click()
        WebDriverWait(self.driver, 10).until(EC.title_is("Create Account | My Store"))

        tax_id = self.driver.find_element(By.CSS_SELECTOR, "[name='tax_id']")
        tax_id.send_keys(u"001")

        company = self.driver.find_element(By.CSS_SELECTOR, "[name='company']")
        company.send_keys(u"ООО Тест")

        firstname = self.driver.find_element(By.CSS_SELECTOR, "[name='firstname']")
        firstname.send_keys(u"Тест")

        lastname = self.driver.find_element(By.CSS_SELECTOR, "[name='lastname']")
        lastname.send_keys(u"Тестович")

        address1 = self.driver.find_element(By.CSS_SELECTOR, "[name='address1']")
        address1.send_keys(u"ул. Пушкина д.111 кв.12")

        address2 = self.driver.find_element(By.CSS_SELECTOR, "[name='address2']")
        address2.send_keys(u"ул. Пушкина д.1")

        postode = self.driver.find_element(By.CSS_SELECTOR, "[name='postcode']")
        postode.send_keys("12345")

        city = self.driver.find_element(By.CSS_SELECTOR, "[name='city']")
        city.send_keys(u"Чикаго")

        country = self.driver.find_element(By.CSS_SELECTOR, "[name='country_code']")
        self.driver.execute_script("arguments[0].selectedIndex = 224; arguments[0].dispatchEvent(new Event('change'))", country)

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[name='zone_code']")))

        state = self.driver.find_element(By.CSS_SELECTOR, "[name='zone_code']")
        self.driver.execute_script("arguments[0].selectedIndex = 224; arguments[0].dispatchEvent(new Event('change'))", state)

        input_email = self.driver.find_element(By.CSS_SELECTOR, "[name='email']")
        email = "test" + datetime.strftime(datetime.now(), "%Y%m%d%H%M%S") + "@test.ru"
        print(email)
        input_email.send_keys(email)

        phone = self.driver.find_element(By.CSS_SELECTOR, "[name='phone']")
        phone.send_keys("12345678")

        input_password = self.driver.find_element(By.CSS_SELECTOR, "[name='password']")
        password = "Qwerty1"
        input_password.send_keys(password)

        confirmed_password = self.driver.find_element(By.CSS_SELECTOR, "[name='confirmed_password']")
        confirmed_password.send_keys("Qwerty1")

        button = self.driver.find_element(By.CSS_SELECTOR, "[name='create_account']")
        button.click()

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#box-account a[href*='logout']")))
        self.driver.find_element(By.CSS_SELECTOR, "#box-account a[href*='logout']").click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#box-account-login")))

        sign_in_online_store(self, email, password)

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#box-account a[href*='logout']")))
        self.driver.find_element(By.CSS_SELECTOR, "#box-account a[href*='logout']").click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#box-account-login")))


    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()