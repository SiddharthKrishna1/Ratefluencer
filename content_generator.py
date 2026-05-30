import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")
def generate_reel_script(topic):
    prompt = f"""Create a 30-60 second viral reel script about: {topic}
    
    Format it as:
    HOOK: (attention grabbing opening line)
    STORY: (main content - 3 key points)
    CTA: (call to action)
    
    Make it engaging, trendy and Gen-Z friendly."""
    
    response = model.generate_content(prompt)
    return response.text

def generate_instagram_caption(topic):
    prompt = f"""Create an Instagram caption for a reel about: {topic}
    Include: catchy first line, 2-3 sentences, 10 relevant hashtags.
    Make it viral-worthy!"""
    
    response = model.generate_content(prompt)
    return response.text

def generate_linkedin_post(topic):
    prompt = f"""Create a professional LinkedIn post about: {topic}
    Include: strong hook, insight, personal angle, call to action.
    Keep it under 200 words."""
    
    response = model.generate_content(prompt)
    return response.text
