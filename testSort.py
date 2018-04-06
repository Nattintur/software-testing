# -*- coding: utf-8 -*-
import unittest

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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

def sort_compare(self, original_list, sorted_list):
    sorted_list.sort()
    for i in range(0, len(original_list)):
        if (original_list[i] != sorted_list[i]):
            return False
    return True

class Sorts(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()


    def test_sort_countries(self):
        self.driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")

        sign_in(self, "admin", "admin")

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dataTable")))

        # проверим сортировку для name
        sorted_list_country = []
        original_list_country = []

        list_td_name = self.driver.find_elements(By.CSS_SELECTOR, ".row td:nth-of-type(5)")
        for i in range(0, len(list_td_name)):
            original_list_country.append(list_td_name[i].text)
            sorted_list_country.append(list_td_name[i].text)



        result = sort_compare(self, original_list_country, sorted_list_country)

        assert result, "Страны отсортированы не в алфавитном порядке"


    def test_zones_sort(self):
        self.driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
        sign_in(self, "admin", "admin")

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dataTable")))

        # проверим сортировку для зон, для стран, где зона != 0
        list_tr = self.driver.find_elements(By.CSS_SELECTOR, ".row")
        list_incorrect_sort_countries = []

        original_list_zone = []
        sorted_list_zone = []

        for i in range(0, len(list_tr)):
            zones_count = (list_tr[i].find_element(By.CSS_SELECTOR, "td:nth-of-type(6)")).text

            # ищем код со значением отличным от 0
            if(str(zones_count) != str(0)):
                list_tr[i].find_element(By.CSS_SELECTOR, "td:nth-of-type(7)").click()
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#table-zones")))

                # получаем список зон
                list_td_zone = self.driver.find_elements(By.CSS_SELECTOR, "#table-zones [name*='[name]'][name*='zones']")
                for j in range(0, len(list_td_zone)):
                    original_list_zone.append(list_td_zone[j].text)
                    sorted_list_zone.append(list_td_zone[j].text)

                # сравниваем список со списком, отсортированным по алфавиту
                result = sort_compare(self, original_list_zone, sorted_list_zone)

                self.driver.find_element(By.CSS_SELECTOR, "[name='cancel']").click()
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dataTable")))

                list_tr = self.driver.find_elements(By.CSS_SELECTOR, ".row")

                if(result == False):
                    country = list_tr[i].find_element(By.CSS_SELECTOR, 'td:nth-of-type(5)').text
                    list_incorrect_sort_countries.append(country)

        if(len(list_incorrect_sort_countries) != 0):
            error_message = "Incorrect sort for codes in country:"

            for j in range(0, len(list_incorrect_sort_countries)):
                    error_message += "\n" + list_incorrect_sort_countries[j]

        assert len(list_incorrect_sort_countries) == 0, error_message


    def test_sort_geo_zones(self):
        self.driver.get("http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones")
        sign_in(self, "admin", "admin")

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dataTable")))
        list_incorrect_sort_countries = []

        list_tr_geo = self.driver.find_elements(By.CSS_SELECTOR, ".row")
        for i in range(0, len(list_tr_geo)):

            original_list_geo_codes = []
            sorted_list_geo_codes = []

            list_tr_geo[i].find_element(By.CSS_SELECTOR, "td:last-of-type").click()
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#table-zones")))

            list_codes_selects = self.driver.find_elements(By.CSS_SELECTOR, "[name*='zones'][name*='[zone_code]']")
            for j in range(len(list_codes_selects)):
                list_option = list_codes_selects[j].find_elements(By.CSS_SELECTOR, "option")
                for k in range(0,len(list_option)):
                    if (list_option[k].is_selected()):
                        original_list_geo_codes.append(list_option[k].text)
                        sorted_list_geo_codes.append(list_option[k].text)
                        break

            result = sort_compare(self, original_list_geo_codes, sorted_list_geo_codes)

            self.driver.find_element(By.CSS_SELECTOR, "[name='cancel']").click()
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dataTable")))

            list_tr_geo = self.driver.find_elements(By.CSS_SELECTOR, ".row")

            if (result == False):
                country = list_tr_geo[i].find_element(By.CSS_SELECTOR, 'td:nth-of-type(5)').text
                list_incorrect_sort_countries.append(country)

        if (len(list_incorrect_sort_countries) != 0):
            error_message = "Incorrect sort for codes in country:"

            for j in range(0, len(list_incorrect_sort_countries)):
                error_message += "\n" + list_incorrect_sort_countries[j]

        assert len(list_incorrect_sort_countries) == 0, error_message

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()