# 🎨 Canva Reviews Analysis
### How do users perceive Canva, and where does it fail them?

An end-to-end analysis of **50,000 Google Play reviews**, built from 
scratch using Python scraping, SQLite, and Looker Studio.

---

## 📌 The Brief

Canva has over 220 million users worldwide and a 4.8 star rating 
on the Google Play Store. But behind that number — what are users 
actually saying?

This project analyses 50,000 real Google Play reviews to answer 
four business questions:

> 1. How do customers perceive Canva's app?
> 2. What problems are users complaining about most?
> 3. Which app versions are generating the most frustration?
> 4. Is Canva actually listening — or just managing its rating?

The goal is not to celebrate what works. It's to find the signal 
inside the noise — the 5,143 frustrated users hidden behind 
a 4.8 star average.

---

## 💡 Key Findings

| # | Finding | Detail |
|---|---------|--------|
| 1 | **84.7% of reviews are positive** | Strong loyal user base — avg score 4.86 |
| 2 | **1,223 users are genuinely frustrated** | Negative score + explicit complaint keyword — crashes, bugs, slow performance |
| 3 | **Performance is the #1 complaint** | "Slow" appears 243 times in negative reviews |
| 4 | **Version 2.335.1 was a problematic release** | Highest complaint rate at 18.9% |
| 5 | **97% response rate — but 99.7% automated** | Only 43 out of 13,087 responses are personalised |

---

## 📦 Dataset

- **Source:** Google Play Store — Canva Android app
- **Collection method:** Python (google-play-scraper library)
- **Size:** 50,000 reviews collected April 2026
- **Features engineered:**
  - `review_type` — positive / neutral / negative (based on score)
  - `has_complaint_keyword` — yes / no (crash, bug, slow, fix...)
  - `has_emoji` — yes / no

> To reproduce data collection: run `scripts/collect_reviews.py`

---

## ⚒️ Methodology
1) Data Collection  → Google Play scraping (Python)
2) Data Cleaning    → Text cleaning, feature engineering (Python)
3) Database Design  → 3-table relational schema (SQLite)
4) SQL Analysis     → 4 business questions
5) Visualisation    → Looker Studio dashboard

---

## 🗄️ SQL Analysis

### The 4 Business Questions
Full queries + inline insights → [`sql/analysis.sql`](sql/analysis.sql)

**Q1 — How do customers perceive Canva's app?**

84.7% of users rate Canva positively. 10.3% left a negative 
review (1-2 stars). Among these, 1,223 contain explicit complaint 
keywords — the most actionable segment for product improvement.

**Q2 — What problems are users complaining about most?**

Performance dominates. "Slow" appears 243 times, "fix" 185 times. 
Combined stability issues (bug + not working + crash) account for 
277 mentions. This is a reliability problem, not a design problem.

**Q3 — Which app versions generate the most complaints?**

Version 2.335.1 peaks at 18.9% negative rate — a likely problematic 
release. Recent versions stabilise around 7-10%.

**Q4 — Is Canva actually listening?**

Canva responds to 96.9% of negative reviews. However, 99.7% of 
those responses are identical automated messages. Only 43 out of 
13,087 responses are personalised.

---

## Dashboard

👉 [View Looker Studio Dashboard](#) ← coming soon

---

## Limitations

- **False negatives:** some 1-2 star reviews contain positive 
  language, likely due to inverted rating scales in Asian markets
- **Version dating:** app version numbers used as chronological 
  proxy — no official release dates available
- **English only:** scraper filtered for English reviews — 
  non-English user feedback not captured

---

## 👩‍💻 About This Project

I'm Celia Breteau, a marketing insights professional transitioning 
into data analytics. After 2 years analysing audience profiles and 
consumer behaviour across 6 industry sectors, I wanted to bring 
that business instinct into a more technical skillset.

This project was built because I genuinely wanted to understand 
what real users think of Canva — not just the headline rating, 
but the frustration behind it. Understanding customer needs has 
always been at the core of my work, and data is just a more 
precise way to do it.
