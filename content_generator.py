import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_reel_script(topic):
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Create a 30-60 second viral reel script about: {topic}
                
                Format it as:
                HOOK: (attention grabbing opening line)
                STORY: (main content - 3 key points)
                CTA: (call to action)
                
                Make it engaging, trendy and Gen-Z friendly."""
            }
        ]
    )
    return message.content[0].text

def generate_instagram_caption(topic):
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": f"""Create an Instagram caption for a reel about: {topic}
                Include: catchy first line, 2-3 sentences, 10 relevant hashtags.
                Make it viral-worthy!"""
            }
        ]
    )
    return message.content[0].text

def generate_linkedin_post(topic):
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": f"""Create a professional LinkedIn post about: {topic}
                Include: strong hook, insight, personal angle, call to action.
                Keep it under 200 words."""
            }
        ]
    )
    return message.content[0].text