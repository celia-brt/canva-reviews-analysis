-- ==============================================
-- CANVA APP REVIEWS ANALYSIS
-- Celia Breteau | Data analytics portefolio
-- Dataset: 50000 Google Play Reviews (Nov 2025 - April 2026)
-- Tools: Python, SQL (SQLite), Text Clustering
-- ==============================================

BUSINESS QUESTION: How do users really experience Canva's mobile app, and where does it fail them ?"

-- ============================
-- Q1 — Overall user perception
-- ============================

SELECT review_type, COUNT(*) as total, 
    ROUND(AVG(score), 2) as avg_score
FROM canva_reviews_clean
GROUP BY review_type
ORDER BY total DESC;

INSIGHT : 
84.7% of users rate Canva positively (avg score: 4.86) — strong loyal user base
However, 5,143 users left negative reviews (avg score of negative review (1 or 2 stars): 1.24)
Among these 5,143 negative reviews, 1,223 contain explicit complaint keywords (crashes, bugs, errors)
These 1,223 users are the most actionable signal — real problems, worth investigating
Limitation: remaining negative reviews (~3,920) may reflect inverted rating scales in Asian markets (users writing "good" but rating 1-2 stars)

-- ================================================
-- -- Q2 — Identifying actionable negative feedback
-- ================================================
    
-- Q2a — Volume of actionable negative reviews
-- ===========================================
    
SELECT COUNT(*) as total_actionable_negative
FROM canva_reviews_clean
WHERE review_type = 'negative'
AND has_complaint_keyword = 'yes';

INSIGHT: 
- 1223 review are truly negative with complaint keywords (2,4% of total)
- These reviews represent high-signal feedback, where users clearly articulate product issues.


-- Q2b — Most frequent complaint themes (keyword-based approach)
-- =============================================================
    
SELECT 
    'crash' as keyword, COUNT(*) as total
FROM canva_reviews_clean
WHERE review_type = 'negative' AND content_clean LIKE '%crash%'
UNION ALL
SELECT 'bug', COUNT(*)
FROM canva_reviews_clean
WHERE review_type = 'negative' AND content_clean LIKE '%bug%'
UNION ALL
SELECT 'slow', COUNT(*)
FROM canva_reviews_clean
WHERE review_type = 'negative' AND content_clean LIKE '%slow%'
UNION ALL
SELECT 'not working', COUNT(*)
FROM canva_reviews_clean
WHERE review_type = 'negative' AND content_clean LIKE '%not working%'
UNION ALL
SELECT 'fix', COUNT(*)
FROM canva_reviews_clean
WHERE review_type = 'negative' AND content_clean LIKE '%fix%'
ORDER BY total DESC;

INSIGHT:
Performance issues dominate negative feedback:
 - "slow" is the most frequent complaint, indicating responsiveness issues
 - "fix" suggests active frustration and expectation of resolution
 - Stability-related issues ("bug", "crash", "not working") are also highly represented

 Overall, complaints point to a **product reliability problem**, rather than missing features.

-- ========================================
-- Q3 - Product stability over app versions
-- ========================================
    
SELECT 
    appVersion,
    total_reviews,
    negative_reviews,
    pct_negative
FROM (
    SELECT 
        appVersion,
        COUNT(*) as total_reviews,
        COUNT(CASE WHEN review_type = 'negative' THEN 1 END) as negative_reviews,
        ROUND(COUNT(CASE WHEN review_type = 'negative' THEN 1 END) * 100.0 / COUNT(*), 1) as pct_negative
    FROM canva_reviews_clean
    WHERE appVersion != ''
    GROUP BY appVersion
    HAVING total_reviews > 10
)
ORDER BY appVersion ASC;

Version numbers used as chronological proxy — higher mid-number = more recent release

INSIGHT: 
- Version 2.342.0 is the most reviewed (6,499 reviews) — highest user exposure
- Version 2.335.1 shows the highest complaint rate (18.9%) — likely a bad release
- Versions 2.337.0 (12.2%) and 2.346.0 (10.0%) also above average

Recent versions stabilize around 7-10% — improvement trend visible

Limitation: 
- Version numbers used as chronological proxy (no release dates available)
- pct_negative includes false negatives from inverted rating scales in Asian markets — 
real complaint rate may be slightly lower

-- =========================================================================
-- Q4a- Does Canva respond to reviews — and does it prioritize negative ones?
-- =========================================================================
    
SELECT 
    canva_reviews_clean.review_type,
    COUNT(canva_reviews_clean.reviewId) as total_reviews,
    COUNT(canva_responses.reviewId) as total_responses,
    ROUND(COUNT(canva_responses.reviewId) * 100.0 / 
        COUNT(canva_reviews_clean.reviewId), 1) as response_rate
FROM canva_reviews_clean
LEFT JOIN canva_responses 
    ON canva_responses.reviewId = canva_reviews_clean.reviewId
GROUP BY canva_reviews_clean.review_type
ORDER BY response_rate DESC;

INSIGHT:
- Canva maintains a very high response rate on negative (~97%) and neutral reviews.
- Positive reviews receive significantly less attention (~13% response rate).
This suggests a reactive support strategy focused on risk management rather than engagement.


-- ======================================================
-- Q4b — Are Canva's responses personalised or templated?
-- ======================================================
    
SELECT 
    CASE WHEN replyContent LIKE '%canva.me/android%' THEN 'templated'
         ELSE 'personalised'
    END as response_type,
    COUNT(*) as total
FROM canva_responses
GROUP BY response_type;

 Only 43 responses are personalised — suggesting an automated response system
-- Positive reviews receive significantly less attention (13.3% response rate)

-- ============================================================
-- FINAL TAKEAWAYS
-- ============================================================

1. Canva benefits from a strong overall perception, but a small segment of users expresses critical issues.
2. Performance and stability are the primary drivers of dissatisfaction.
3. Certain app versions show clear spikes in negative feedback, indicating release-related issues.
4. Canva responds at scale but relies heavily on automated messaging.
     
→ Key opportunity: improve product reliability and enhance the quality of user support interactions.
