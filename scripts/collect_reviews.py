from google_play_scraper import reviews, Sort
import csv

result, _ = reviews(
    'com.canva.editor',
    lang='en',
    country='au',
    sort=Sort.NEWEST,
    count=50000
)

# Deduplicate by reviewId
seen = set()
unique_reviews = []
for r in result:
    if r['reviewId'] not in seen:
        seen.add(r['reviewId'])
        unique_reviews.append(r)

keys = ['reviewId', 'userName', 'score', 'at', 'content', 
        'thumbsUpCount', 'replyContent', 'repliedAt', 'appVersion']

with open('canva_reviews_raw.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(unique_reviews)

print(f"Total unique reviews: {len(unique_reviews)} ✅")
