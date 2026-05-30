import re

def calculate_virality_score(topic, script):
    """
    ML-inspired multi-factor virality scoring engine.
    Analyzes content across 6 dimensions to predict viral potential.
    Returns score (0-100) with detailed breakdown.
    """

    scores = {}

    # ── 1. HOOK STRENGTH (0-20) ──────────────────────────────
    hook_score = 10
    power_words = [
        "secret", "shocking", "nobody", "finally", "truth", "exposed",
        "breaking", "viral", "insane", "hack", "warning", "revealed",
        "stop", "never", "always", "fastest", "easiest", "mistake",
        "proven", "guaranteed", "urgent", "limited", "exclusive"
    ]
    topic_lower = topic.lower()
    script_lower = script.lower()

    for word in power_words:
        if word in topic_lower or word in script_lower[:200]:
            hook_score += 2
    hook_score = min(hook_score, 20)
    scores["Hook Strength"] = hook_score

    # ── 2. CONTENT DEPTH (0-20) ──────────────────────────────
    depth_score = 0
    word_count = len(script.split())
    if word_count > 100: depth_score += 5
    if word_count > 200: depth_score += 5
    if word_count > 300: depth_score += 5

    structure_keywords = ["hook", "story", "cta", "insight", "tip", "step", "point"]
    for kw in structure_keywords:
        if kw in script_lower:
            depth_score += 1
    depth_score = min(depth_score, 20)
    scores["Content Depth"] = depth_score

    # ── 3. TREND ALIGNMENT (0-20) ────────────────────────────
    trend_score = 10
    trend_topics = [
        "ai", "artificial intelligence", "machine learning", "chatgpt", "llm",
        "startup", "creator economy", "passive income", "side hustle",
        "productivity", "mental health", "crypto", "web3", "automation",
        "remote work", "elon", "openai", "tesla", "apple", "google"
    ]
    for trend in trend_topics:
        if trend in topic_lower or trend in script_lower:
            trend_score += 2
    trend_score = min(trend_score, 20)
    scores["Trend Alignment"] = trend_score

    # ── 4. EMOTIONAL TRIGGER (0-15) ──────────────────────────
    emotion_score = 5
    emotions = {
        "curiosity": ["why", "how", "what if", "did you know", "imagine"],
        "fear": ["danger", "risk", "warning", "mistake", "losing", "fail"],
        "inspiration": ["success", "achieve", "transform", "change", "possible"],
        "humor": ["lol", "funny", "joke", "crazy", "wild", "unbelievable"]
    }
    for emotion_type, words in emotions.items():
        for word in words:
            if word in script_lower:
                emotion_score += 1
                break
    emotion_score = min(emotion_score, 15)
    scores["Emotional Trigger"] = emotion_score

    # ── 5. CTA STRENGTH (0-15) ───────────────────────────────
    cta_score = 5
    cta_words = ["follow", "share", "like", "comment", "save", "subscribe",
                 "click", "link", "dm", "tag", "repost", "download"]
    for word in cta_words:
        if word in script_lower:
            cta_score += 2
    cta_score = min(cta_score, 15)
    scores["CTA Strength"] = cta_score

    # ── 6. HASHTAG & PLATFORM FIT (0-10) ─────────────────────
    platform_score = 5
    if "#" in script: platform_score += 3
    hashtag_count = script.count("#")
    if hashtag_count >= 5: platform_score += 2
    platform_score = min(platform_score, 10)
    scores["Platform Fit"] = platform_score

    # ── FINAL SCORE ───────────────────────────────────────────
    total = sum(scores.values())
    total = min(total, 100)

    return total, scores


def get_influencer_score(profile: dict) -> dict:
    """
    ML-inspired Ratefluencer Score™ for influencer ranking.
    Input: profile dict with engagement metrics
    Output: score (0-100) with breakdown
    """
    scores = {}

    followers = profile.get("followers", 10000)
    following = profile.get("following", 500)
    avg_likes = profile.get("avg_likes", 500)
    avg_comments = profile.get("avg_comments", 50)
    avg_shares = profile.get("avg_shares", 20)
    avg_saves = profile.get("avg_saves", 30)
    posts_per_week = profile.get("posts_per_week", 3)
    fake_follower_pct = profile.get("fake_follower_pct", 10)

    # Engagement Rate Score (0-25)
    engagement_rate = ((avg_likes + avg_comments + avg_shares + avg_saves) / max(followers, 1)) * 100
    if engagement_rate >= 6:
        eng_score = 25
    elif engagement_rate >= 3:
        eng_score = 18
    elif engagement_rate >= 1:
        eng_score = 10
    else:
        eng_score = 5
    scores["Engagement Rate"] = eng_score

    # Authenticity Score (0-25)
    auth_score = max(0, 25 - int(fake_follower_pct * 0.5))
    scores["Authenticity"] = auth_score

    # Posting Consistency (0-20)
    if posts_per_week >= 5:
        consistency = 20
    elif posts_per_week >= 3:
        consistency = 15
    elif posts_per_week >= 1:
        consistency = 8
    else:
        consistency = 3
    scores["Consistency"] = consistency

    # Audience Quality (0-15)
    ff_ratio = followers / max(following, 1)
    if ff_ratio >= 10:
        audience_score = 15
    elif ff_ratio >= 3:
        audience_score = 10
    else:
        audience_score = 5
    scores["Audience Quality"] = audience_score

    # Save Rate (0-15) — high saves = strong evergreen content
    save_rate = (avg_saves / max(followers, 1)) * 100
    if save_rate >= 2:
        save_score = 15
    elif save_rate >= 0.5:
        save_score = 10
    else:
        save_score = 5
    scores["Save Rate"] = save_score

    total = sum(scores.values())
    total = min(total, 100)

    return {"total": total, "breakdown": scores, "engagement_rate": round(engagement_rate, 2)}
