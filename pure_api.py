import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from yaml import SafeLoader

from explore_tags import explore_tags, Stats
from login_util import login
from selenium.webdriver.chrome.options import Options


with open('config.yml') as f:
    config = yaml.load(f, Loader=SafeLoader)


def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get("https://www.instagram.com")
    return driver


if __name__ == '__main__':
    driver = setup_driver()
    login(driver=driver, username=config['username'], password=config['password'])

    try:
        explore_tags(driver, config['tags'], config['comments'])
    except Exception as e:
        raise e
    finally:
        Stats.print_stats()
