import pandas as pd
from collections import Counter
import re

# -------------------------
# STOP WORDS
# -------------------------
stop_words = set([
    'this', 'that', 'have', 'with', 'when', 'they', 'from', 'your',
    'will', 'been', 'just', 'some', 'very', 'also', 'more', 'than',
    'into', 'what', 'which', 'about', 'after', 'like', 'make', 'even',
    'much', 'only', 'then', 'most', 'cant', 'dont', 'does', 'please',
    'canva', 'good', 'great', 'love', 'nice', 'app', 'use', 'used'
])

# -------------------------
# NEGATIVE WORDS
# -------------------------
negative_words = [
    'crash', 'bug', 'error', 'fail', 'issue', 'problem',
    'slow', 'lag', 'freeze', 'glitch',
    'expensive', 'price', 'subscription',
    'difficult', 'hard', 'confusing',
    'hate', 'annoying', 'bad', 'worst', 'terrible'
]

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv('/Users/celiabreteau/Documents/DATA/Project_canva/data/verbatims_clustered.csv')

# enlever le bruit
df = df[df['cluster'] != -1]

# -------------------------
# FUNCTIONS
# -------------------------
def clean_text(texts):
    text = ' '.join(texts).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

def top_words(texts, n=7):
    text = clean_text(texts)
    words = text.split()
    
    words = [
        w for w in words 
        if len(w) > 3 and w not in stop_words
    ]
    
    return [word for word, _ in Counter(words).most_common(n)]

def negative_score(texts):
    text = clean_text(texts)
    return sum(text.count(word) for word in negative_words)

# -------------------------
# BUILD SUMMARY
# -------------------------
summary_list = []

for cluster, group in df.groupby('cluster'):
    texts = group['Text'].astype(str).tolist()
    
    summary_list.append({
        'cluster': cluster,
        'count': len(texts),
        'top_words': top_words(texts),
        'negative_score': negative_score(texts),
        'sample': texts[0]
    })

summary = pd.DataFrame(summary_list)

# score relatif (IMPORTANT)
summary['negativity_ratio'] = summary['negative_score'] / summary['count']

# tri par frustration
summary = summary.sort_values('negativity_ratio', ascending=False)

# label lisible
summary['insight'] = summary['top_words'].apply(lambda x: ' / '.join(x))

# -------------------------
# SAVE
# -------------------------
summary.to_csv('/Users/celiabreteau/Documents/DATA/Project_canva/data/cluster_summary.csv', index=False)

# -------------------------
# OUTPUT
# -------------------------
print("Top 10 most negative clusters:\n")
print(summary[['cluster', 'count', 'negativity_ratio', 'insight', 'sample']].head(10))
