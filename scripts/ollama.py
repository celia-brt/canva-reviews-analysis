import pandas as pd
import requests

df = pd.read_csv('/Users/celiabreteau/Documents/DATA/Project_canva/data/canva_reviews_final.csv')

# Filtrer seulement les négatives avec complaint
mask = (df['review_type'] == 'negative') & (df['has_complaint_keyword'] == 'yes')
negative_df = df[mask].copy()

print(f"Reviews to summarize: {len(negative_df)}")

# Initialiser la colonne
df['content_summary'] = df['content']

def summarize(text):
    if not isinstance(text, str) or len(text) < 30:
        return text
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'qwen2.5:3b',
                'prompt': f'In maximum 10 words, what is the main complaint in this review? Reply with only the sentence, nothing else: {text}',
                'stream': False
            },
            timeout=30
        )
        result = response.json().get('response', '').strip()
        # Vérifier que c'est bien un résumé pas une troncature
        if len(result) > 10:
            return result
        return text
    except:
        return text

count = 0
for idx in negative_df.index:
    text = df.loc[idx, 'content']
    df.loc[idx, 'content_summary'] = summarize(text)
    count += 1
    if count % 50 == 0:
        print(f"Progress: {count}/{len(negative_df)}")

df.to_csv('/Users/celiabreteau/Documents/DATA/Project_canva/data/canva_reviews_final.csv', index=False)
print(f"Done ✅ — {count} reviews summarized")
