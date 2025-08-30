import time
import random
import logging
import pandas as pd
from urllib.parse import urljoin
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from datetime import datetime

# --- Logging ---
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# --- Setup Chrome ---
chrome_path = r"C:\Users\Ghiffari\Documents\chromedriver-win64\chromedriver.exe"
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

service = Service(executable_path=chrome_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
base_url = 'https://nitter.net/search?f=tweets&q=%22MPKMB+lang%3Aid+since%3A2024-06-30+until%3A2024-11-10%22'


# --- DataFrame setup ---
df = pd.DataFrame(columns=["username", "date", "tweet"])

# --- Helper function ---
def to_date(date_str):
    return datetime.strptime(date_str, "%b %d, %Y · %I:%M %p UTC")

try:
    # Step 1: Open nitter
    logging.info("Opening nitter.net")
    driver.get("https://nitter.net")
    time.sleep(random.randint(3, 6))

    # Step 2: Search query
    logging.info("Searching for query...")
    search_input = driver.find_element(By.NAME, 'q')
    query = 'MPKMB lang:id since:2024-06-30 until:2024-11-10'
    search_input.send_keys(query)
    search_input.send_keys(Keys.RETURN)
    time.sleep(5)  # allow page to fully load

    # Step 3: Scraping Loop
    logging.info("Starting scraping loop")
    end_scraping = False
    while not end_scraping:

        tweets = driver.find_elements(By.CSS_SELECTOR, "div.timeline-item")

        if not tweets:
            logging.info("No tweets found on this page, stopping.")
            break

        for tweet in tweets:
            try:
                username = tweet.find_element(By.CSS_SELECTOR, "a.username").text
                date_text = tweet.find_element(By.CSS_SELECTOR, "span.tweet-date > a").get_attribute("title").strip()
                content = tweet.find_element(By.CSS_SELECTOR, "div.tweet-content").text.strip()

                tweet_date = to_date(date_text)

                if tweet_date.date() < datetime(2024, 6, 30).date():
                    logging.info("Reached the earliest date limit, stopping.")
                    end_scraping = True
                    break

                df = pd.concat([df, pd.DataFrame([{
                    "username": username,
                    "date": tweet_date.strftime("%Y-%m-%d %H:%M"),
                    "tweet": content
                }])], ignore_index=True)

            except Exception as e:
                logging.warning(f"Skipped a tweet due to error: {e}")

        # Step 4: Go to next page if exists
        if not end_scraping:
            try:
                show_more = driver.find_element(By.XPATH, '//a[contains(text(), "Load more")]')
                next_href = show_more.get_attribute("href")

                # extract cursor
                cursor_match = re.search(r'cursor=([^&]+)', next_href)
                if cursor_match:
                    cursor_value = cursor_match.group(1)
                    next_url = base_url + f"&cursor={cursor_value}"
                    print(f"[INFO] Next page detected with cursor: {cursor_value}")

                    driver.get(next_url)
                    time.sleep(random.uniform(3, 6))
                else:
                    print("[INFO] Cursor not found, scraping finished.")
                    break
            except Exception as e:
                print(f"[INFO] Next page not found or error: {e}")
                break

    # Step 5: Export CSV
    output_path = "scraped_tweets.csv"
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    logging.info(f"Scraping finished. Total collected: {len(df)} tweets.")
    logging.info(f"Data exported to {output_path}")

finally:
    driver.quit()
