import pickle
from pathlib import Path
from time import sleep

from selenium import webdriver
import yaml
from selenium.webdriver.common.by import By
from yaml.loader import SafeLoader
import json

# Open the file and load the file
with open('xpath.yml') as f:
    xpath_dict = yaml.load(f, Loader=SafeLoader)


def login(driver: webdriver.Chrome, username, password):
    if Path('cookies.pkl').is_file():
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        return
    # if Path('cookies.json').is_file():
    #     with open('cookies.json', 'r') as cookie_file:
    #         cookies = json.load(cookie_file)
    #         for key in cookies:
    #             driver.add_cookie({'name': key, 'value': cookies[key]})
    #         sleep(2)
    #         driver.get("https://www.instagram.com")
    #         return
    sleep(1)
    accept_cookies = driver.find_element(By.XPATH, xpath_dict['accept_cookies'])
    accept_cookies.click()
    sleep(2)
    username_e = driver.find_element(By.XPATH, xpath_dict['username'])
    username_e.send_keys(username)
    sleep(1)
    username_e = driver.find_element(By.XPATH, xpath_dict['password'])
    username_e.send_keys(password)
    sleep(1)
    login_button = driver.find_element(By.XPATH, xpath_dict['login_button'])
    login_button.click()
    sleep(5)
    save_login = driver.find_element(By.XPATH, xpath_dict['save_login'])
    save_login.click()
    sleep(5)
    turn_on_notif = driver.find_element(By.XPATH, xpath_dict['turn_on_notif'])
    turn_on_notif.click()
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
