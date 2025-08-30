import time
import random
import pandas as pd
from urllib.parse import urljoin
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from datetime import datetime


chrome_path = r"C:\Users\Ghiffari\Documents\chromedriver-win64\chromedriver.exe"
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

service = Service(executable_path=chrome_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
base_url = 'https://nitter.net/search?f=tweets&q=%23TNIAD+lang%3Aid+since%3A2025-03-10+until%3A2025-03-29+-filter%3Aretweets'


df = pd.DataFrame(columns=["username", "date", "tweet"])

def to_date(date_str):
    return datetime.strptime(date_str, "%b %d, %Y · %I:%M %p UTC")

try:
    print("Opening nitter.net")
    driver.get("https://nitter.net")
    time.sleep(random.randint(3, 6))

    print("Searching for query...")
    search_input = driver.find_element(By.NAME, 'q')
    query = '#TNIAD lang:id since:2025-03-10 until:2025-03-29 -filter:retweets'
    search_input.send_keys(query)
    search_input.send_keys(Keys.RETURN)
    time.sleep(5)  # allow page to fully load

    print("Starting scraping loop")
    end_scraping = False
    while not end_scraping:

        tweets = driver.find_elements(By.CSS_SELECTOR, "div.timeline-item")

        if not tweets:
            print("No tweets found on this page, stopping.")
            break

        for tweet in tweets:
            try:
                fullname = tweet.find_element(By.CSS_SELECTOR, "a.fullname").text
                username = tweet.find_element(By.CSS_SELECTOR, "a.username").text
                date_text = tweet.find_element(By.CSS_SELECTOR, "span.tweet-date > a").get_attribute("title").strip()
                content = tweet.find_element(By.CSS_SELECTOR, "div.tweet-content").text.strip()

                tweet_date = to_date(date_text)

                if len(df) >= 11000:
                    print("Reached the earliest date limit, stopping.")
                    end_scraping = True
                    break

                df = pd.concat([df, pd.DataFrame([{
                    "fullname": fullname,
                    "username": username,
                    "date": tweet_date.strftime("%Y-%m-%d %H:%M"),
                    "tweet": content
                }])], ignore_index=True)

            except Exception as e:
                print(f"Skipped a tweet due to error: {e}")

        if not end_scraping:
            try:
                show_more = driver.find_element(By.XPATH, '//a[contains(text(), "Load more")]')
                next_href = show_more.get_attribute("href")

                cursor_match = re.search(r'cursor=([^&]+)', next_href)
                if cursor_match:
                    cursor_value = cursor_match.group(1)
                    next_url = base_url + f"&cursor={cursor_value}"
                    print(f"[INFO] Next page detected with cursor: {cursor_value}\n\n")
                    print(f"already get {len(df)} rows")

                    driver.get(next_url)
                    time.sleep(random.uniform(1, 3))
                else:
                    print("[INFO] Cursor not found, scraping finished.")
                    break
            except Exception as e:
                print(f"[INFO] Next page not found or error: {e}")
                break

    output_path = "scraped_tniad_tweets.csv"
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Scraping finished. Total collected: {len(df)} tweets.")
    print(f"Data exported to {output_path}")

finally:
    driver.quit()
