from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

def _call(prompt, max_tokens=1024):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

def generate_reel_script(topic):
    return _call(f"""You are a viral content strategist for top creators.
Create a 30-60 second viral reel script about: {topic}

Format EXACTLY as:
🎣 HOOK: (1 punchy line that stops the scroll)
📖 STORY:
  Point 1: (key insight)
  Point 2: (surprising fact or stat)
  Point 3: (practical tip)
📢 CTA: (strong call to action)

Make it Gen-Z friendly, high energy, and impossible to skip.""")

def generate_instagram_caption(topic):
    return _call(f"""You are an Instagram growth expert.
Create a viral Instagram caption for a reel about: {topic}

Include:
- Scroll-stopping first line (no emojis at start)
- 2-3 engaging sentences
- Question to boost comments
- 15 trending hashtags grouped by size

Format neatly with line breaks.""", max_tokens=512)

def generate_linkedin_post(topic):
    return _call(f"""You are a LinkedIn thought leader with 500k followers.
Write a viral LinkedIn post about: {topic}

Structure:
- Bold hook line
- Personal story or insight (3-4 lines)
- 3 key takeaways as bullet points
- Engagement question
- 5 relevant hashtags

Keep under 220 words. Professional but conversational.""", max_tokens=512)

def generate_trend_analysis(topic):
    return _call(f"""You are a trend analyst for a top marketing agency.
Analyze this trending topic: {topic}

Provide:
1. WHY IT'S TRENDING: (2 sentences)
2. TARGET AUDIENCE: (who cares most)
3. BEST PLATFORMS: (where to post)
4. CONTENT ANGLE: (unique angle to stand out)
5. BRAND OPPORTUNITY: (how brands can use this)

Be specific and data-driven.""", max_tokens=512)

def generate_brand_match(topic, niche):
    return _call(f"""You are an influencer marketing consultant.
For a creator posting about: {topic}
In the niche: {niche}

Recommend 5 ideal brand partnerships:
For each brand provide:
- Brand Name
- Match Score: X/100
- Why they match
- Campaign idea (1 line)

Format as a clean list.""", max_tokens=512)
