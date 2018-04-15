# -*- coding: utf-8 -*-
import unittest

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

class LinksToNewPages(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost/litecart/admin")

    def test_links(self):
        wait = WebDriverWait(self.driver, 10)
        sign_in(self, "admin", "admin")

        self.driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")

        self.driver.find_element(By.CSS_SELECTOR, "#content a.button[href*='?app=countries&doc=edit_country']").click()

        links = self.driver.find_elements(By.CSS_SELECTOR, "#content .fa-external-link")

        original_window = self.driver.current_window_handle
        # print(original_window)
        old_windows = self.driver.window_handles
        # print(old_windows)

        for i in range(len(links)):
            links[i].click()
            wait.until(EC.new_window_is_opened(old_windows))
            # wait.until(EC.number_of_windows_to_be(2))

            windows = self.driver.window_handles
            # print(windows)

            for j in range(len(windows)):
                if windows[j] != original_window:
                    new_window = windows[j]
                    break

            self.driver.switch_to.window(new_window)
            # print(self.driver.current_window_handle)

            self.driver.close()
            self.driver.switch_to.window(original_window)
            # print(original_window)


    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
