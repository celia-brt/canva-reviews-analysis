import pandas as pd

# ============================================
# STEP 1 — Load files
# ============================================
reviews = pd.read_csv('/Users/celiabreteau/Documents/DATA/Project_canva/data/Canva_reviews_clean.csv')
clusters = pd.read_csv('/Users/celiabreteau/Documents/DATA/Project_canva/data/verbatims_clustered.csv')
summary = pd.read_csv('/Users/celiabreteau/Documents/DATA/Project_canva/data/cluster_summary_clean.csv', sep=';', decimal=',')

print(f"Reviews: {len(reviews)}")
print(f"Clusters before dedup: {len(clusters)}")

# ============================================
# STEP 2 — Deduplicate clusters
# ============================================
clusters_dedup = clusters.drop_duplicates(subset='Text', keep='first')
print(f"Clusters after dedup: {len(clusters_dedup)}")

# ============================================
# STEP 3 — Merge reviews + clusters
# ============================================
merged = reviews.merge(clusters_dedup[['Text', 'cluster']], 
                       left_on='content_clean', 
                       right_on='Text', 
                       how='left')

print(f"Merged: {len(merged)} rows")
print(f"Unmatched: {merged['cluster'].isna().sum()}")

# ============================================
# STEP 4 — Merge cluster summary
# ============================================
summary_slim = summary[['cluster', 'negativity_ratio', 'negative_score']].copy()
merged = merged.merge(summary_slim, on='cluster', how='left')

# ============================================
# STEP 5 — Theme labels
# ============================================
theme_map = {
    251: 'App Access Issues',
    239: 'Slow Performance',
    253: 'App Not Working',
    246: 'Text Editing Friction',
    247: 'Video Download Speed',
    240: 'Billing & Refund Issues',
    252: 'Network Connectivity',
    211: 'Difficult to Use',
    243: 'Download Speed',
    250: 'Poor Mobile Experience',
    218: 'Missing Onboarding',
    242: 'Pricing & Premium',
    64:  'Negative Experience',
    237: 'Free vs Premium Frustration'
}
merged['theme'] = merged['cluster'].map(theme_map).fillna('Other')

# ============================================
# STEP 6 — Priority labels
# ============================================
priority_map = {
    'App Not Working': 'Critical',
    'Video Download Speed': 'High',
    'Billing & Refund Issues': 'High',
    'Slow Performance': 'High',
    'App Access Issues': 'High',
    'Download Speed': 'Medium',
    'Free vs Premium Frustration': 'Medium',
    'Pricing & Premium': 'Medium',
    'Difficult to Use': 'Medium',
    'Text Editing Friction': 'Low',
    'Missing Onboarding': 'Low',
    'Poor Mobile Experience': 'Low',
    'Network Connectivity': 'Low'
}
merged['priority'] = merged['theme'].map(priority_map).fillna('Low')

# ============================================
# STEP 7 — Numeric columns
# ============================================
merged['has_complaint_keyword_num'] = merged['has_complaint_keyword'].map({'yes': 1, 'no': 0})
merged['has_emoji_num'] = merged['has_emoji'].map({'yes': 1, 'no': 0})
merged['has_reply'] = merged['replyContent'].apply(
    lambda x: 1 if isinstance(x, str) and x.strip() != '' else 0
)
merged['is_negative'] = merged['review_type'].apply(lambda x: 1 if x == 'negative' else 0)
merged['is_positive'] = merged['review_type'].apply(lambda x: 1 if x == 'positive' else 0)
merged['is_neutral'] = merged['review_type'].apply(lambda x: 1 if x == 'neutral' else 0)

# ============================================
# STEP 8 — Date columns
# ============================================
merged['Date'] = pd.to_datetime(merged['at'], dayfirst=True).dt.strftime('%Y-%m-%d')
merged['month'] = pd.to_datetime(merged['Date']).dt.strftime('%Y-%m')

# ============================================
# STEP 9 — Summary
# ============================================
print(f"\nReply distribution:")
print(merged.groupby('review_type')['has_reply'].mean().round(3) * 100)
print(f"\nTheme distribution:")
print(merged['theme'].value_counts().head(15))
print(f"\nPriority distribution:")
print(merged['priority'].value_counts())

# ============================================
# STEP 10 — Save
# ============================================
merged.to_csv('/Users/celiabreteau/Documents/DATA/Project_canva/data/canva_reviews_final.csv', 
              index=False, quoting=1)

print(f"\nDone ✅ — {len(merged)} rows saved")
