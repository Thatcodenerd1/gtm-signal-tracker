"""
Urgency Scoring Model
Scores signals 0-100 based on type and recency.
"""

from datetime import datetime, timedelta

BASE_SCORES = {
    'leadership_change': 90,
    'funding': 85,
    'hiring_signal': 70,
    'market_expansion': 65,
    'tech_change': 55,
    'general_news': 20
}

def score_signal(signal_type, published_at, decay_days=30):
    base = BASE_SCORES.get(signal_type, 20)
    try:
        pub_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
        age_days = (datetime.now().astimezone() - pub_date).days
        recency_factor = max(0, 1 - (age_days / decay_days))
    except Exception:
        recency_factor = 0.5
    score = int(base * (0.6 + 0.4 * recency_factor))
    return min(100, max(0, score))

def get_tier(score):
    if score >= 80:
        return 'HIGH'
    elif score >= 60:
        return 'MEDIUM'
    elif score >= 40:
        return 'LOW'
    return 'NOISE'
