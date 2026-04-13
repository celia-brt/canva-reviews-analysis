CANVA APP REVIEWS
Celia Breteau | Data analytics portefolio
--------------------------------------------
Dataset: 50000 Google Play Reviews (2026)
Tools: Python, SQL
--------------------------------------------
QUESTION: "How do users perceive Canva, and where does it fail them ?"


-- Q1 - How do customers perceive Canva's app ? 

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


-- Q2 - What complaint keywords appear most frequently in negative reviews?

-- Q2a — Volume of actionable negative reviews
SELECT COUNT(*) as total_actionable_negative
FROM canva_reviews_clean
WHERE review_type = 'negative'
AND has_complaint_keyword = 'yes';

INSIGHT: 1223 review are truly negative with complaint keywords (2,4% of total)

-- Q2b — What complaint keywords appear most frequently in negative reviews?

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
Top complaint = "slow" (243) - performance is Canva's #1 pain point
"fix" (185) suggests users are demanding action — frustration is active, not passive
"bug" (101) + "not working" (89) + "crash" (87) = 277 stability complaints combined
Performance & stability account for the majority of explicit complaints
This is a product reliability signal, not a design or feature issue

-- Q3 - Which app versions generate the most complaints?

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
 INSIGHT:
- Version 2.342.0 is the most reviewed (6,499 reviews) — highest user exposure
- Version 2.335.1 shows the highest complaint rate (18.9%) — likely a bad release
- Versions 2.337.0 (12.2%) and 2.346.0 (10.0%) also above average

Recent versions stabilize around 7-10% — improvement trend visible

Limitation: 
- Version numbers used as chronological proxy (no release dates available)
- pct_negative includes false negatives from inverted rating scales in Asian markets — 
real complaint rate may be slightly lower

-- Q4- Does Canva respond to reviews — and does it prioritize negative ones?

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
- Canva responds to 96.9% of negative reviews — near-perfect response rate
- Canva responds to 97.1% of neutral reviews — treating 3-star as a risk signal
- Canva responds to only 13.3% of positive reviews — not a priority

-- Q4b — Are Canva's responses personalised or templated?
SELECT 
    CASE WHEN replyContent LIKE '%canva.me/android%' THEN 'templated'
         ELSE 'personalised'
    END as response_type,
    COUNT(*) as total
FROM canva_responses
GROUP BY response_type;

 Only 43 responses are personalised — suggesting an automated response system
-- Positive reviews receive significantly less attention (13.3% response rate)