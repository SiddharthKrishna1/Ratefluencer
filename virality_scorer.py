def calculate_virality_score(topic, script):
    score = 50  # base score
    
    # Check for viral elements
    viral_words = ["breaking", "shocking", "secret", "viral", 
                   "amazing", "nobody", "finally", "truth", "exposed"]
    
    topic_lower = topic.lower()
    script_lower = script.lower()
    
    for word in viral_words:
        if word in topic_lower or word in script_lower:
            score += 5
    
    # Length bonus
    if len(script) > 300:
        score += 10
    
    # Cap at 100
    score = min(score, 100)
    
    return score