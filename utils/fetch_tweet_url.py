from selenium.webdriver.common.by import By
import re
from selenium.webdriver.common.keys import Keys


def fetch_tweet(driver, last_tweet_link):
    # Define the URL of the Twitter page you want to scrape
    url = "https://twitter.com/DBSparkingZER0"

    # Navigate to the Twitter page
    driver.get(url)

    # Give the page some time to load

    # driver.execute_script("window.scrollTo(0, 4000);")
    driver.implicitly_wait(10)
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    body.send_keys(Keys.PAGE_DOWN)

    # Find all tweet texts
    tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')

    tweet_link_pattern = re.compile(r'https://x\.com/.+?/status/\d+$')

    # Loop through tweets and extract the text
    for tweet in tweets:
        pinned_divs = tweet.find_elements(
            By.XPATH, './/div[contains(text(), "Pinned")]')
        if pinned_divs:
            continue
        anchor_tags = tweet.find_elements(By.TAG_NAME, 'a')
        hrefs = [anchor.get_attribute('href') for anchor in anchor_tags]
        tweet_link = list(filter(tweet_link_pattern.match, hrefs))[0]
        if last_tweet_link == tweet_link:
            return None
        return tweet_link
