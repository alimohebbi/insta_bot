import random
from time import sleep
import yaml
from selenium import webdriver
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
    follow = 0

    @classmethod
    def print_stats(cls):
        print(f'Likes: {Stats.likes}, Comments: {Stats.comments}, Follows: {Stats.follow}')


def explore_tags(driver: webdriver.Chrome, tag_list, comment_list):
    sleep(2)
    for tag_i in range(len(tag_list)):
        tag = random.choice(tag_list)
        try:
            iterate_tag_posts(comment_list, driver, tag)
        except Exception as e:
            print(f'Tag "{tag}" raised an error: {e}')
        print(f'Tag "{tag}" finished')
        Stats.print_stats()


def iterate_tag_posts(comment_list, driver, tag):
    driver.get(f'https://www.instagram.com/explore/tags/{tag}/')
    sleep(5)
    click(driver, xpath_dict['first_media'])
    for page in range(random.randint(1, config['max_next_limit'])):
        post_operations(comment_list, driver)
        click(driver, xpath_dict['next_button'])


def post_operations(comment_list, driver):
    if random.uniform(0, 1) < config['like_ratio']:
        Stats.likes += 1
        click(driver, xpath_dict['like_button'])
    if random.uniform(0, 1) < config['comment_ratio']:
        Stats.comments += 1
        send_keys(driver, xpath_dict['comment_area'], random.choice(comment_list))
        click(driver, xpath_dict['post_button'])
    if random.uniform(0, 1) < config['follow_ratio']:
        try:
            click(driver, xpath_dict['follow_button'])
            Stats.follow += 1
        except Exception as e:
            print('Cannot follow')
