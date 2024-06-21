from selenium.webdriver.common.by import By
import re
from selenium.webdriver.common.keys import Keys
from utils.login import login
import time


def scroll_down(driver, times=1):
    body = driver.find_element(By.TAG_NAME, 'body')
    for _ in range(times):
        body.send_keys(Keys.PAGE_DOWN)
        # Adjust the sleep time as necessary to ensure tweets are loaded
        # time.sleep(2)


def fetch_tweet(driver, last_tweet_link, username="DBSparkingNews"):
    # Define the URL of the Twitter page you want to scrape
    url = f"https://x.com/{username}"

    # Navigate to the Twitter page
    driver.get(url)

    # Give the page some time to load

    # driver.execute_script("window.scrollTo(0, 4000);")
    driver.implicitly_wait(10)
    time.sleep(2)
    # scroll_down(driver, 2)
    # test_tweet = driver.find_element(By.CSS_SELECTOR, '[data-testid="tweet"]')

    # Find all tweet texts
    tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')

    tweet_link_pattern = re.compile(r'https://x\.com/.+?/status/\d+$')

    # Loop through tweets and extract the text
    for tweet in tweets:
        pinned_divs = tweet.find_elements(
            By.XPATH, './/div[contains(text(), "Pinned")]')

        anchor_tags = tweet.find_elements(By.TAG_NAME, 'a')
        hrefs = [anchor.get_attribute('href') for anchor in anchor_tags]
        tweet_link = list(filter(tweet_link_pattern.match, hrefs))[0]
        if pinned_divs:
            continue
        if last_tweet_link == tweet_link:
            return None
        return tweet_link


if __name__ == "__main__":
    driver = login()
    time.sleep(5)
    print(fetch_tweet(driver, None))
    time.sleep(20)
    # driver.quit()
