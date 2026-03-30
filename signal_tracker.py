"""
GTM Signal Tracker — Main Script
Monitors company news to surface buying signals for a target account list.
"""

import os
import csv
import json
import argparse
from datetime import datetime, timedelta
from utils.news_fetcher import fetch_news
from classifiers import classify_signal
from scorer import score_signal

def load_accounts(filepath):
    accounts = []
    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            accounts.append(row)
    return accounts

def run_tracker(accounts_path, days=7, signal_types=None, output=None):
    accounts = load_accounts(accounts_path)
    since = datetime.now() - timedelta(days=days)
    results = []

    for account in accounts:
        company = account.get('company') or account.get('name', '')
        domain = account.get('domain', '')
        print(f"  Checking signals for: {company}")

        articles = fetch_news(company, domain, since)
        for article in articles:
            signal_type = classify_signal(article['title'], article['description'])
            if signal_types and signal_type not in signal_types:
                continue
            score = score_signal(signal_type, article['published_at'])
            results.append({
                'company': company,
                'signal_type': signal_type,
                'headline': article['title'][:80],
                'score': score,
                'date': article['published_at'][:10],
                'url': article['url']
            })

    results.sort(key=lambda x: x['score'], reverse=True)

    if output:
        with open(output, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print(f"\nSaved {len(results)} signals to {output}")
    else:
        print(f"\n{'Company':<20} {'Signal Type':<20} {'Score':<8} {'Date':<12} {'Headline'}")
        print('-' * 90)
        for r in results[:20]:
            print(f"{r['company']:<20} {r['signal_type']:<20} {r['score']:<8} {r['date']:<12} {r['headline']}")

    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GTM Signal Tracker')
    parser.add_argument('--accounts', required=True, help='Path to target_accounts.csv')
    parser.add_argument('--days', type=int, default=7, help='Lookback window in days')
    parser.add_argument('--signal-type', help='Filter: hiring,funding,expansion,leadership,tech')
    parser.add_argument('--output', help='Output CSV path')
    args = parser.parse_args()

    signal_types = args.signal_type.split(',') if args.signal_type else None
    print(f"Running GTM Signal Tracker — last {args.days} days")
    run_tracker(args.accounts, args.days, signal_types, args.output)
