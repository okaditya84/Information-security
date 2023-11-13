'''
v1.0 tests for secretary - https://secretary-password-manager.herokuapp.com/
powered by https://github.com/lia0wang
'''
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from time import sleep
import os

# user dict
num = random.randint(50,100)
user_dict = {
    "user_name": f"BOT_LEON_{num}",
    "email": f"botleon{num}@secretarytesting.com",
    "password": "iamabot",
    "password2": "iamabot"
}

# A global dictionary to store the websites.
my_websites = {
    "local": "http://127.0.0.1:8001/",
}

new_passwords = {
    "google_pw": [
        "https://www.google.com",
        "lia0wang@outlook.com",
        "google123"
    ],
    "github_pw": [
        "https://github.com",
        "lia0wang@outlook.com",
        "github123"
    ],
}

# A class to store the websites information
def setup_driver():
    # Initialise options.
    options = Options()
    options.add_argument("--window-size=0.5920,0.5200")
    options.headless = False
    # Find the path of chrome.
    path = GeckoDriverManager().install()
    driver = webdriver.Firefox(options=options, executable_path=path, service_log_path=os.devnull)
    # login_linkedin(driver, user_dict)
    return driver

# auto clicker for my websites
def go_web_page(driver, website):
    # go to my websites
    driver.get(website)
    sleep(1)

def register(driver, user_dict):
    driver.find_element_by_xpath("/html/body/header/nav/ul/li[3]/a").click()
    sleep(1)
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/form/input[2]").send_keys(user_dict["user_name"])
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/form/input[3]").send_keys(user_dict["email"])
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/form/input[4]").send_keys(user_dict["password"])
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/form/input[5]").send_keys(user_dict["password2"])
    sleep(0.5)
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/form/input[6]").click()
    sleep(1)

def add_password(driver, new_passwords):
    for pasword in new_passwords:
        driver.find_element_by_xpath("/html/body/header/nav/ul/li[4]/a").click()
        sleep(1)
        driver.find_element_by_xpath("/html/body/div[2]/div[3]/form/input[2]").send_keys(new_passwords[pasword][0])
        driver.find_element_by_xpath("/html/body/div[2]/div[3]/form/input[3]").send_keys(new_passwords[pasword][1])
        driver.find_element_by_xpath("/html/body/div[2]/div[3]/form/input[4]").send_keys(new_passwords[pasword][2])
        sleep(0.5)
        driver.find_element_by_xpath("/html/body/div[2]/div[3]/form/input[5]").click()
        sleep(0.5)
        sleep(1)

def go_view_then_go_home(driver):
    driver.find_element_by_xpath("/html/body/header/nav/ul/li[3]/a").click()
    sleep(1)
    driver.find_element_by_xpath("/html/body/header/nav/ul/li[1]/a").click()
    sleep(1)

def log_out(driver):
    driver.find_element_by_xpath("/html/body/header/nav/ul/li[2]/a").click()
    sleep(1)

def verify_password_email(driver, new_passwords):
    decrypt_email_1 = driver.find_element_by_xpath("/html/body/div[3]/div[1]/input[1]").get_attribute("value")
    decrypt_password_1 = driver.find_element_by_xpath("/html/body/div[3]/div[1]/input[2]").get_attribute("value")
    decrypt_email_2 = driver.find_element_by_xpath("/html/body/div[3]/div[2]/input[1]").get_attribute("value")
    decrypt_password_2 = driver.find_element_by_xpath("/html/body/div[3]/div[2]/input[2]").get_attribute("value")

    assert decrypt_email_1 == new_passwords["github_pw"][1]
    assert decrypt_password_1 == new_passwords["github_pw"][2]
    assert decrypt_email_2 == new_passwords["google_pw"][1]
    assert decrypt_password_2 == new_passwords["google_pw"][2]
    print("User email and password are correct.")
    sleep(1)

def delete_password(driver):
    driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[1]/i").click()
    sleep(0.5)
    driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[1]/a").click()
    sleep(1)

def run():
    driver = setup_driver()
    go_web_page(driver, my_websites["local"])
    register(driver, user_dict)
    add_password(driver, new_passwords)
    verify_password_email(driver, new_passwords)
    delete_password(driver)
    go_view_then_go_home(driver)
    log_out(driver)
    # driver.close()

if __name__ == "__main__":
    run()
