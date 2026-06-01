def calculate_virality_score(topic, script):
    """
    AI-powered multi-factor virality scoring engine.
    Analyzes content across 6 dimensions to predict viral potential.
    Returns score (0-100) with detailed breakdown.
    """
    scores = {}
    topic_lower = topic.lower()
    script_lower = script.lower()

    hook_score = 10
    power_words = [
        "secret", "shocking", "nobody", "finally", "truth", "exposed",
        "breaking", "viral", "insane", "hack", "warning", "revealed",
        "stop", "never", "always", "fastest", "easiest", "mistake",
        "proven", "guaranteed", "urgent", "limited", "exclusive",
    ]
    for word in power_words:
        if word in topic_lower or word in script_lower[:200]:
            hook_score += 2
    scores["Hook Strength"] = min(hook_score, 20)

    depth_score = 0
    word_count = len(script.split())
    if word_count > 100:
        depth_score += 5
    if word_count > 200:
        depth_score += 5
    if word_count > 300:
        depth_score += 5
    for keyword in ["hook", "story", "cta", "insight", "tip", "step", "point"]:
        if keyword in script_lower:
            depth_score += 1
    scores["Content Depth"] = min(depth_score, 20)

    trend_score = 10
    trend_topics = [
        "ai", "artificial intelligence", "machine learning", "chatgpt", "llm",
        "startup", "creator economy", "passive income", "side hustle",
        "productivity", "mental health", "crypto", "web3", "automation",
        "remote work", "openai", "tesla", "apple", "google",
    ]
    for trend in trend_topics:
        if trend in topic_lower or trend in script_lower:
            trend_score += 2
    scores["Trend Alignment"] = min(trend_score, 20)

    emotion_score = 5
    emotions = {
        "curiosity": ["why", "how", "what if", "did you know", "imagine"],
        "fear": ["danger", "risk", "warning", "mistake", "losing", "fail"],
        "inspiration": ["success", "achieve", "transform", "change", "possible"],
        "humor": ["lol", "funny", "joke", "crazy", "wild", "unbelievable"],
    }
    for words in emotions.values():
        if any(word in script_lower for word in words):
            emotion_score += 1
    scores["Emotional Trigger"] = min(emotion_score, 15)

    cta_score = 5
    for word in ["follow", "share", "like", "comment", "save", "subscribe", "click", "link", "dm", "tag", "repost", "download"]:
        if word in script_lower:
            cta_score += 2
    scores["CTA Strength"] = min(cta_score, 15)

    platform_score = 5
    hashtag_count = script.count("#")
    if hashtag_count:
        platform_score += 3
    if hashtag_count >= 5:
        platform_score += 2
    scores["Platform Fit"] = min(platform_score, 10)

    return min(sum(scores.values()), 100), scores
