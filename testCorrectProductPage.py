# -*- coding: utf-8 -*-
import unittest

import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import *


class CorrectProductPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

        # Запуск по-новому, FF последней версии для gecodriver 0.20
        # self.driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver', capabilities={"marionette":True})

        ## версия FF
        # self.driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver', capabilities={"marionette": True})

        self.driver.get("http://localhost/litecart")

    # а)
    def test_product_text(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#box-campaigns")))

        products_campaigns = self.driver.find_elements(By.CSS_SELECTOR, "#box-campaigns .product")
        first_product_name = products_campaigns[0].find_element(By.CSS_SELECTOR, ".name").text

        products_campaigns[0].click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#box-product h1.title")))

        product_name = self.driver.find_element(By.CSS_SELECTOR, "#box-product h1.title").text

        assert first_product_name == product_name

    # б)
    def test_product_price(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#box-campaigns")))

        products_campaigns = self.driver.find_elements(By.CSS_SELECTOR, "#box-campaigns .product")
        first_product_regular_price = products_campaigns[0].find_element(By.CSS_SELECTOR, ".regular-price").text
        first_product_campaign_price= products_campaigns[0].find_element(By.CSS_SELECTOR, ".campaign-price").text

        products_campaigns[0].click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#box-product .price-wrapper")))

        product_regular_price = self.driver.find_element(By.CSS_SELECTOR, "#box-product .regular-price").text
        product_campaign_price = self.driver.find_element(By.CSS_SELECTOR, "#box-product .campaign-price").text

        is_regular_price_correct = first_product_regular_price == product_regular_price
        is_campaign_price_correct = first_product_campaign_price == product_campaign_price

        assert is_regular_price_correct or is_campaign_price_correct, "Цены не соответствуют тем, что указаны на главной странице"
        assert is_regular_price_correct, "Обычная цена не соответствует той, что указана на главной странице"
        assert is_campaign_price_correct, "Аукционная цена не соответствует той, что указана на главной странице"

    # в)
    def test_style_price(self):
        # для главной
        products_campaigns = self.driver.find_elements(By.CSS_SELECTOR, "#box-campaigns .product")
        first_product_regular_price_strikethrough = products_campaigns[0].find_element(By.CSS_SELECTOR, ".regular-price").get_attribute("tagName")

        is_first_product_regular_price_strikethrough = str(first_product_regular_price_strikethrough).lower() == "s"

        first_product_regular_price_color = products_campaigns[0].find_element(By.CSS_SELECTOR, ".regular-price").value_of_css_property("color")

        result = re.search("\((\d+)\D+(\d+)\D+(\d+)", first_product_regular_price_color)

        is_first_product_regular_price_color = result.group(1) == result.group(2) and result.group(2) == result.group(3)

        assert is_first_product_regular_price_strikethrough or is_first_product_regular_price_color, "На главной странице цвет текста для обычной цены не соответствует серому и незачеркнут"

        assert is_first_product_regular_price_strikethrough, "На главной странице текст для обычной цены незачеркнут"

        assert is_first_product_regular_price_color, "На главной странице цвет текста для обычной цены несерый"

    # г)
    def test_style_campaign_price(self):
        # для главной
        products_campaigns = self.driver.find_elements(By.CSS_SELECTOR, "#box-campaigns .product")
        first_product_campaign_price_bold = products_campaigns[0].find_element(By.CSS_SELECTOR, ".campaign-price").get_attribute("tagName")

        is_first_product_campaign_price_bold = str(first_product_campaign_price_bold).lower() == "strong"

        first_product_campaign_price_color = products_campaigns[0].find_element(By.CSS_SELECTOR, ".campaign-price").value_of_css_property("color")
        # print(first_product_campaign_price_color)

        result = re.search("\((\d+)\D+(\d+)\D+(\d+)", first_product_campaign_price_color)

        is_first_product_campaign_price_color = int(result.group(2)) == 0 and int(result.group(3)) == 0 and int(result.group(1)) != 0

        error_message = ""

        if (is_first_product_campaign_price_bold != True):
            error_message = "На главной странице текст для аукционной цены нежирного начертания"

        if (is_first_product_campaign_price_color != True):
            error_message = "На главной странице цвет текста для аукционной цены некрасный"

        if (is_first_product_campaign_price_bold != True and is_first_product_campaign_price_color != True):
            error_message = "На главной странице цвет текста для аукционой цены не соответствует красному и текст нежирный"

        # для продуктовой

        products_campaigns[0].click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#box-product .price-wrapper")))

        product_campaign_price_color = self.driver.find_element(By.CSS_SELECTOR, ".campaign-price").value_of_css_property("color")

        result = re.search("\((\d+)\D+(\d+)\D+(\d+)", product_campaign_price_color)

        is_product_campaign_price_color = int(result.group(2)) == 0 and int(result.group(3)) == 0 and int(result.group(1)) != 0

        assert len(error_message) == 0, error_message
        assert is_product_campaign_price_color, "На продуктовой странице цвет текста для аукционной цены некрасный"

    # д)
    def test_style_prise_size(self):
        # для главной
        products_campaigns = self.driver.find_elements(By.CSS_SELECTOR, "#box-campaigns .product")
        first_product_regular_price_size = products_campaigns[0].find_element(By.CSS_SELECTOR, ".regular-price").size["height"]
        first_product_campaign_price_size = products_campaigns[0].find_element(By.CSS_SELECTOR, ".campaign-price").size["height"]

        error_message = ""

        if(first_product_campaign_price_size < first_product_regular_price_size):
            error_message = "На главной странице аукционная цена некрупнее, чем обычная"

        products_campaigns[0].click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#box-product .price-wrapper")))

        product_regular_price_size = self.driver.find_element(By.CSS_SELECTOR, ".regular-price").size["height"]
        product_campaign_price_size = self.driver.find_element(By.CSS_SELECTOR, ".campaign-price").size["height"]

        assert len(error_message) == 0, error_message
        assert product_campaign_price_size > product_regular_price_size, "На продуктовой странице аукционная цена некрупнее, чем обычная"


    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()