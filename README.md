# GTM Signal Tracker

A Python tool that monitors company news to surface buying signals for a target account list — helping GTM teams reach the right company with the right message at the right moment.

## The Problem

Most outbound teams send the same message to everyone. High-performing GTM teams use *triggers* — a company just raised funding, hired a new VP of Sales, or announced an expansion — to reach out with a message that's actually relevant right now. This tool automates that signal detection.

## How It Works

```
Input: target_accounts.csv (company name, domain, industry)
         ↓
Signal Detection: NewsAPI + RSS feeds + keyword matching
         ↓
Classification: Hiring signal / Funding / Expansion / Tech change / Leadership change
         ↓
Scoring: Urgency score based on signal type + recency
         ↓
Output: trigger_report.csv + outreach_priorities.csv
```

## Signal Types Detected

| Signal | Example | Urgency |
|--------|---------|---------|
| Leadership change | New VP of Marketing hired | High |
| Funding round | Series B announced | High |
| Headcount expansion | 50+ new job postings | Medium |
| Market expansion | New office or product region | Medium |
| Tech stack change | New tool adoption (Salesforce, HubSpot) | Low-Medium |

## Setup

```bash
pip install requests pandas textblob nltk python-dotenv
python -m nltk.downloader punkt stopwords

# Add your NewsAPI key to .env
echo "NEWS_API_KEY=your_key_here" > .env
```

## Usage

```bash
# Basic run — check signals for your account list
python signal_tracker.py --accounts target_accounts.csv --days 7

# Output trigger report to CSV
python signal_tracker.py --accounts target_accounts.csv --days 14 --output trigger_report.csv

# Filter by signal type
python signal_tracker.py --accounts target_accounts.csv --signal-type hiring,funding
```

## Output Example

```
Company          Signal Type       Headline                               Score   Date
Acme Corp        Leadership change  Acme Corp names new Chief Revenue...   92      2026-03-20
BetaCo           Funding           BetaCo raises $45M Series B to exp...   88      2026-03-18
GammaTech        Hiring signal     GammaTech opens 40 new sales roles...   71      2026-03-22
```

## Files

```
gtm-signal-tracker/
├── signal_tracker.py        # Main signal detection engine
├── classifiers.py           # Signal type classification logic
├── scorer.py                # Urgency scoring model
├── utils/
│   ├── news_fetcher.py      # NewsAPI + RSS ingestion
│   └── keyword_matcher.py   # NLP-based keyword extraction
├── target_accounts.csv      # Sample input file
└── requirements.txt
```

## Background

Built as a practical tool to systematize the account prioritization work I did at Social Capital Inc., where I manually tracked buying signals to decide which accounts to prioritize in outreach. The original manual process took 2-3 hours/week; this script runs in under 2 minutes.

---

*Part of [Mansi More's GTM & Growth Portfolio](https://github.com/Thatcodenerd1/gtm-growth-projects)*
