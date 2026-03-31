"""
Signal Classification Logic
Classifies news articles into GTM signal types based on keyword matching.
"""

SIGNAL_PATTERNS = {
    'leadership_change': [
        'appoints', 'names', 'hires', 'joins as', 'new cro', 'new cmo', 'new vp',
        'new chief', 'promoted to', 'head of sales', 'head of marketing', 'svp of'
    ],
    'funding': [
        'raises', 'series a', 'series b', 'series c', 'seed round', 'funding round',
        'investment', 'venture capital', 'valuation', 'unicorn', 'ipo', 'spac'
    ],
    'hiring_signal': [
        'hiring', 'we\'re growing', 'join our team', 'open roles', 'expanding team',
        'headcount', 'new positions', 'recruiting', 'talent acquisition', 'job postings'
    ],
    'market_expansion': [
        'expands to', 'launches in', 'enters market', 'new market', 'international',
        'opens office', 'new region', 'new vertical', 'product launch', 'new product'
    ],
    'tech_change': [
        'adopts', 'integrates', 'partners with', 'deploys', 'implements',
        'salesforce', 'hubspot', 'snowflake', 'datadog', 'okta', 'platform migration'
    ]
}

def classify_signal(title, description=''):
    text = (title + ' ' + (description or '')).lower()
    scores = {}
    for signal_type, keywords in SIGNAL_PATTERNS.items():
        count = sum(1 for kw in keywords if kw in text)
        if count > 0:
            scores[signal_type] = count
    if not scores:
        return 'general_news'
    return max(scores, key=scores.get)

def get_signal_label(signal_type):
    labels = {
        'leadership_change': 'Leadership Change',
        'funding': 'Funding Round',
        'hiring_signal': 'Hiring Signal',
        'market_expansion': 'Market Expansion',
        'tech_change': 'Tech Stack Change',
        'general_news': 'General News'
    }
    return labels.get(signal_type, signal_type)
