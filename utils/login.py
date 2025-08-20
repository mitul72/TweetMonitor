from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from dotenv import load_dotenv
import os

load_dotenv()  # Load the .env file


def load_cookie(driver):
    driver.add_cookie({
        'name': 'auth_token',
        'value': os.getenv('AUTH_TOKEN'),
    })
    driver.add_cookie({
        'name': 'ct0',
        'value': os.getenv('CT0'),
    })


def login():
    # Set up the Selenium WebDriver with headless options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    # # Overcome limited resource problems
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    try:
        # Define the URL of the Twitter page you want to scrape
        url = "https://x.com/i/flow/login"
        driver.get(url)
        load_cookie(driver)

        # # Find the username and password fields
        # username_field = driver.find_element(
        #     By.CSS_SELECTOR, 'input[autocomplete="username"]')
        # username_field.send_keys(os.getenv('EMAIL'))
        # button = driver.find_element(
        #     By.XPATH, '//button[.//span[text()="Next"]]')
        # button.click()
        # time.sleep(2)
        # password_field = driver.find_element(
        #     By.CSS_SELECTOR, 'input[autocomplete="current-password"]')
        # password_field.send_keys(os.getenv('PASSWORD'))
        # button = driver.find_element(
        #     By.XPATH, '//button[.//span[text()="Log in"]]')
        # button.click()
        # time.sleep(5)
        print("Logged in successfully")
    except Exception as e:
        print(f"Failed to log in: {e}")

    return driver


if __name__ == '__main__':
    login()
