import pandas as pd
import re

# Load raw data
df = pd.read_csv('/Users/celiabreteau/Documents/DATA/Project_canva/data/canva_reviews_raw.csv')

print(f"Reviews loaded: {len(df)}")

# --- CLEANING ---
def clean_text(text):
    if not isinstance(text, str):
        return ''
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.strip()
    return text

df['content_clean'] = df['content'].apply(clean_text)

# --- REVIEW TYPE based on score ---
df['review_type'] = df['score'].apply(lambda x:
    'negative' if x <= 2 else
    'neutral'  if x == 3 else
    'positive'
)

# --- COMPLAINT KEYWORDS ---
keywords = [
    'crash', 'bug', 'fix', 'not working', 'broken',
    'slow', 'problem', 'issue', 'cant', 'unable',
    'error', 'glitch', 'freeze', 'loading', 'failed'
]

exclude_phrases = ['no problem', 'no issue', 'no bug', 'no crash']

df['has_complaint_keyword'] = df['content_clean'].apply(
    lambda x: 'no' if any(e in str(x) for e in exclude_phrases)
    else ('yes' if any(k in str(x) for k in keywords) else 'no')
)

# --- HAS EMOJI FLAG ---
def has_emoji(text):
    if not isinstance(text, str):
        return 'no'
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F9FF"
        u"\U00002700-\U000027BF"
        "]+", flags=re.UNICODE)
    return 'yes' if emoji_pattern.search(text) else 'no'

df['has_emoji'] = df['content'].apply(has_emoji)

# --- SAVE ---
df.to_csv('/Users/celiabreteau/Documents/DATA/Project_canva/data/canva_reviews_clean.csv', index=False)

# --- SUMMARY ---
print(f"\nReview type distribution:")
print(df['review_type'].value_counts())

print(f"\nComplaint keywords detected:")
print(df['has_complaint_keyword'].value_counts())

print(f"\nReviews with emoji:")
print(df['has_emoji'].value_counts())

print(f"\nColumns in final dataset:")
print(df.columns.tolist())
