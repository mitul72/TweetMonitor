from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
from selenium.webdriver.common.keys import Keys

# Set up the Selenium WebDriver with headless options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
# # Overcome limited resource problems
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

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
    tweet_text = tweet.text
    print(f"Tweet: {tweet_link}")
# Close the WebDriver
# driver.quit()
