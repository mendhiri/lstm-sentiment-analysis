from google_play_scraper import reviews, Sort
import pandas as pd

all_reviews = []
app_id = 'com.gojek.gopay'
count_target = 90000
batch_size = 100 
token = None

while len(all_reviews) < count_target:
    rvs, token = reviews(
        app_id,
        lang='id',
        country='id',
        sort=Sort.MOST_RELEVANT,
        count=batch_size,
        continuation_token=token  
    )
    all_reviews.extend(rvs)
    if token is None:
        break  # Sudah habis

df = pd.DataFrame(all_reviews[:count_target])  
df.to_csv('ulasan_aplikasi.csv', index=False)