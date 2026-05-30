import os
import json

from dotenv import load_dotenv

try:
    from groq import Groq
except ImportError:
    Groq = None

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
client = Groq(api_key=GROQ_API_KEY) if Groq and GROQ_API_KEY else None


def _call(prompt, max_tokens=1024):
    if Groq is None:
        return "Groq package is not installed. Run pip install -r requirements.txt to enable live AI generation."
    if client is None:
        return "Groq API is not configured. Add GROQ_API_KEY to enable live AI generation."

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


def _fallback_reel_package(topic, audience="creators and marketers", tone="high-energy"):
    hashtags = [
        "#CreatorEconomy", "#ContentStrategy", "#ViralReels", "#AIContent",
        "#MarketingTips", "#TrendAlert", "#ShortFormVideo", "#GrowthStrategy",
    ]
    scenes = [
        {
            "time": "0-3s",
            "visual": "Fast zoom on a phone showing a spike in trend activity.",
            "on_screen_text": "This trend is moving fast",
            "voiceover": f"If you create for {audience}, do not ignore this: {topic}.",
            "broll_prompt": f"Vertical cinematic phone screen with social trend analytics for {topic}",
        },
        {
            "time": "3-12s",
            "visual": "Creator highlights three quick insight cards on screen.",
            "on_screen_text": "Why it matters",
            "voiceover": "The audience is already curious, brands are looking for angles, and early explainers can own the conversation.",
            "broll_prompt": f"Creator desk setup, floating insight cards, topic: {topic}",
        },
        {
            "time": "12-24s",
            "visual": "Split-screen showing problem, insight, and practical takeaway.",
            "on_screen_text": "Turn it into a simple story",
            "voiceover": "Start with the change, show what people misunderstand, then give one practical move viewers can use today.",
            "broll_prompt": f"Vertical split-screen content storyboard about {topic}",
        },
        {
            "time": "24-35s",
            "visual": "Bold closing frame with save/share prompt.",
            "on_screen_text": "Save this before it peaks",
            "voiceover": "Save this idea, make it your own, and post while the trend still has momentum.",
            "broll_prompt": f"Minimal vertical end card for a viral reel about {topic}",
        },
    ]
    voiceover_script = "\n".join(scene["voiceover"] for scene in scenes)
    return {
        "title": f"Reel: {topic}",
        "duration": "35 seconds",
        "tone": tone,
        "target_audience": audience,
        "hook": scenes[0]["voiceover"],
        "scenes": scenes,
        "voiceover_script": voiceover_script,
        "subtitles": [scene["voiceover"] for scene in scenes],
        "thumbnail_prompt": f"Vertical reel thumbnail, bold readable title, subject: {topic}, modern creator economy style",
        "instagram_caption": f"{topic} is a content window creators can use right now.\n\nWhat angle would you post first?\n\n{' '.join(hashtags)}",
        "linkedin_post": f"{topic} is more than a trend. It is a signal for creators and brands to test faster, explain clearer, and publish while attention is still forming.\n\nThree moves:\n- Find the misconception\n- Turn it into a simple story\n- Add a practical takeaway\n\nWhat trend are you watching this week?",
        "hashtags": hashtags,
    }


def _json_from_model(prompt, max_tokens=1600):
    text = _call(prompt, max_tokens=max_tokens)
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return json.loads(text[start:end])
    except (ValueError, json.JSONDecodeError):
        return None


def generate_reel_video_package(topic, audience="creators and marketers", tone="high-energy"):
    prompt = f"""You are an AI short-form video director building an automated reel package.
Topic: {topic}
Audience: {audience}
Tone: {tone}

Return valid JSON only with these keys:
title, duration, tone, target_audience, hook, scenes, voiceover_script, subtitles, thumbnail_prompt, instagram_caption, linkedin_post, hashtags.

Requirements:
- The reel must be 30-60 seconds.
- scenes must contain 4 objects.
- Each scene object must have time, visual, on_screen_text, voiceover, broll_prompt.
- Voiceover must be ready for text-to-speech.
- Subtitles must match the voiceover.
- Captions and hashtags must be ready to publish.
- Make every output specifically about the selected topic."""
    package = _json_from_model(prompt)
    if not package:
        return _fallback_reel_package(topic, audience, tone)
    return package
