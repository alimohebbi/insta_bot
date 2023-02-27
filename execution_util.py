from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By


def click(driver: webdriver.Chrome, xpath):
    element = driver.find_element(By.XPATH, xpath)
    element.click()
    sleep(5)


def send_keys(driver: webdriver.Chrome, xpath, text):
    element = driver.find_element(By.XPATH, xpath)
    element.click()
    sleep(2)
    element = driver.find_element(By.XPATH, xpath)
    element.send_keys(text)
