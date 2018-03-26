# -*- coding: utf-8 -*-
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def is_element_present(self, *args):
  try:
    self.driver.find_element(*args)
    return True
  except NoSuchElementException:
    return False


def sign_in(self, user, password_user):

    assert(is_element_present(self, By.NAME, 'username'))
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


class SignInAdmin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        # self.driver.implicitly_wait(30)
        try:
            self.driver.get("http://localhost/litecart/admin")
        except:
            pass

    def test_left_menu(self):

        WebDriverWait(self.driver, 10).until(EC.title_is("My Store"))

        sign_in(self, "admin", "admin")

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='fa-sign-out']")))

        current_outer_index = 0
        list_menu = self.driver.find_elements(By.ID, "app-")

        while (current_outer_index < len(list_menu)):
            list_menu[current_outer_index].click()

            assert (is_element_present(self, By.TAG_NAME, 'h1'))

            current_inner_index = 0

            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[id*='doc-']")))
                sub_menu = self.driver.find_elements(By.CSS_SELECTOR, "[id*='doc-']")
            except TimeoutException:
                sub_menu = ""

            while(current_inner_index < len(sub_menu)):


                sub_menu[current_inner_index].click()
                assert (is_element_present(self, By.TAG_NAME, 'h1'))

                current_inner_index = current_inner_index+1

                sub_menu = self.driver.find_elements(By.CSS_SELECTOR, "[id*='doc-']")

            current_outer_index = current_outer_index + 1

            list_menu = self.driver.find_elements(By.ID, "app-")


    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
