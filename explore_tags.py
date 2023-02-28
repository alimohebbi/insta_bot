import json
import random
import traceback
from datetime import datetime
from pathlib import Path
from time import sleep
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from yaml.loader import SafeLoader

# Open the file and load the file
from execution_util import click, send_keys

with open('xpath.yml') as f:
    xpath_dict = yaml.load(f, Loader=SafeLoader)

with open('config.yml') as f:
    config = yaml.load(f, Loader=SafeLoader)


class Stats:
    likes = 0
    comments = 0
    follows = 0
    reached_users = set()
    operations_hourly_limit = 0

    @classmethod
    def load_reached_users(cls):
        if Path('users.json').is_file():
            with open('users.json', 'r') as user_files:
                Stats.reached_users = set(json.load(user_files))

    @classmethod
    def add_user_id(cls, user):
        if user in Stats.reached_users:
            return False
        Stats.reached_users.add(user)
        with open('users.json', 'w') as outfile:
            json.dump(list(Stats.reached_users), outfile)
        return True

    @classmethod
    def print_stats(cls):
        print(f'Likes: {Stats.likes}, Comments: {Stats.comments}, Follows: {Stats.follows}')

    @classmethod
    def hourly_limit(cls):
        return max(cls.likes, cls.comments, cls.follows) > config['operation_per_hour_limit']

    @classmethod
    def clear_stats(cls):
        cls.likes, cls.comments, cls.follows = 0, 0, 0


def explore_tags(driver: webdriver.Chrome, tag_list, comment_list):
    Stats.load_reached_users()
    sleep(2)
    for tag_i in range(len(tag_list)):
        tag = random.choice(tag_list)
        try:
            iterate_tag_posts(comment_list, driver, tag)
        except Exception as e:
            traceback.print_exc()
            print(f'Tag "{tag}" raised an error: {e}')

        print(f'Tag "{tag}" finished')
        Stats.print_stats()


def add_insta_id(driver):
    element = driver.find_element(By.XPATH, xpath_dict['user_id'])
    return Stats.add_user_id(element.text)


def iterate_tag_posts(comment_list, driver, tag):
    driver.get(f'https://www.instagram.com/explore/tags/{tag}/')
    sleep(5)
    click(driver, xpath_dict['first_media'])
    for page in range(random.randint(1, config['max_next_limit'])):
        if (add_insta_id(driver)):
            post_operations(comment_list, driver)
        click(driver, xpath_dict['next_button'])


def check_operation_limits():
    if Stats.hourly_limit():
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print(f'{dt_string} Hourly operations exceeded. I sleep {config["sleep_time"]} seconds.')
        sleep(config["sleep_time"])
        Stats.clear_stats()
        print('I wake up!')


def post_operations(comment_list, driver):
    check_operation_limits()
    if random.uniform(0, 1) < config['follow_ratio']:
        try:
            click(driver, xpath_dict['follow_button'])
            Stats.follows += 1
        except Exception as e:
            print('Cannot follow')
    if random.uniform(0, 1) < config['like_ratio']:
        Stats.likes += 1
        click(driver, xpath_dict['like_button'])
    if random.uniform(0, 1) < config['comment_ratio']:
        Stats.comments += 1
        send_keys(driver, xpath_dict['comment_area'], random.choice(comment_list))
        click(driver, xpath_dict['post_button'])
