# Ratefluencer AI Reel Agent

Track 2 prototype for the Ratefluencer AI Hackathon 2026: **AI Viral Reel Creator Agent**.

The app discovers trending topics, ranks them, generates a ready-to-post reel package, renders a vertical reel preview, exports a downloadable MP4, and predicts virality before publishing.

## Problem Statement

Creators spend too much time finding trends, writing hooks, planning reels, creating captions, editing videos, and guessing whether content will perform. This project automates that workflow with an AI agent that turns a selected topic into a complete short-form content package.

## Selected Hackathon Track

**Track 2: AI Viral Reel Creator Agent**

The project focuses on:

- Trending topic discovery
- Trend ranking
- Reel script generation
- Automated reel planning
- Voiceover-ready script generation
- Captions and subtitles
- Thumbnail and B-roll prompts
- MP4 reel export
- Instagram caption generation
- LinkedIn post generation
- Virality prediction before publishing
- Performance feedback learning loop

## Features

- **Trend Discovery Engine**: Fetches current trend candidates for AI, technology, business, startups, finance, and creator economy.
- **Trend Ranking Engine**: Assigns trend score, growth proxy, source, and confidence signals.
- **AI Reel Generator**: Produces a 30-60 second reel package based on the selected topic.
- **Video Preview**: Shows an animated vertical reel-style preview inside the app.
- **MP4 Export**: Renders the generated scene plan into a downloadable vertical MP4 reel with subtitles.
- **Voiceover and Subtitles**: Generates text-to-speech ready voiceover and matching subtitle lines.
- **Visual Asset Planning**: Creates scene-by-scene visuals, thumbnail prompt, and B-roll prompts.
- **Publishing Copy**: Generates Instagram caption, hashtags, and LinkedIn post.
- **Virality Prediction**: Scores the generated reel across hook strength, content depth, trend alignment, emotional trigger, CTA strength, and platform fit.
- **Learning Loop**: Captures post-publish performance feedback for future recommendation tuning.
- **Agent Workflow Logs**: Displays the autonomous steps executed during the current run.
- **Downloadable Output**: Exports both JSON and MP4 outputs.

## Tech Stack

- Python
- Streamlit
- Groq API
- LLaMA 3.3 70B configurable through environment variables
- NewsAPI for trend discovery
- HTML/CSS animation for the reel preview
- PIL, NumPy, ImageIO, and FFmpeg for MP4 rendering

## Project Structure

```text
ratefluencer-agent/
├── app.py                # Streamlit UI and Track 2 workflow
├── content_generator.py  # AI reel package generation
├── trend_finder.py       # Trend discovery and ranking
├── virality_scorer.py    # Virality prediction logic
├── video_renderer.py     # Vertical MP4 reel rendering
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Setup Instructions

1. Clone or open the project folder.

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
NEWS_API_KEY=your_newsapi_key
GROQ_MODEL=llama-3.3-70b-versatile
```

`GROQ_MODEL` is optional. If it is not set, the app uses `llama-3.3-70b-versatile`.

4. Run the app:

```bash
streamlit run app.py
```

## API Keys

### Required for live AI generation

- `GROQ_API_KEY`

Without this key, the app still returns a local fallback reel package so the demo does not break.

### Required for live trend discovery

- `NEWS_API_KEY`

Without this key, the app clearly shows that live trend data is unavailable and allows manual topic entry.

## How to Use

1. Open the Streamlit app.
2. Go to **Reel Generator**.
3. Select a trend category:
   - Artificial Intelligence
   - Technology
   - Business
   - Startups
   - Finance
   - Creator Economy
4. Select a live topic or enter a manual topic.
5. Choose target audience and reel tone.
6. Click **Generate AI Reel**.
7. Review:
   - Animated AI video preview
   - Hook
   - Voiceover script
   - Scene-by-scene visual plan
   - Subtitles
   - Thumbnail prompt
   - B-roll prompts
   - Instagram caption
   - LinkedIn post
   - Virality score
8. Download the reel package JSON.
9. Click **Render MP4 Reel**.
10. Preview and download the generated `.mp4` file.

## AI Workflow

```text
Trend Discovery Agent
        |
Trend Ranking Engine
        |
Script Generation Agent
        |
Automated Reel Generator
        |
Video Rendering Agent
        |
Publishing Agent
        |
Virality Prediction Engine
        |
Learning Loop
```

## Data Flow

```text
NewsAPI / Manual Topic
        |
Selected Trending Topic
        |
Groq LLaMA Prompt
        |
Structured Reel Package JSON
        |
Animated Preview + MP4 Export + Publishing Assets
        |
Virality Score + Performance Feedback
```

## Virality Scoring

The virality engine scores content from 0 to 100 using:

- Hook Strength
- Content Depth
- Trend Alignment
- Emotional Trigger
- CTA Strength
- Platform Fit

The app also estimates:

- Expected views
- Expected likes
- Expected shares
- Expected saves

## Hackathon Deliverables Covered

- Source code
- README
- Setup instructions
- Streamlit working prototype
- AI workflow
- Data flow
- Reel generation pipeline
- Trend discovery system
- Downloadable MP4 reel output
- Virality prediction system
- Performance learning loop
- Ready-to-demo user interface

## Demo Script

1. Start on the **Reel Generator** page.
2. Explain that the project solves Track 2: automating the content creation workflow for creators.
3. Select a category such as **Artificial Intelligence** or **Creator Economy**.
4. Pick a trending topic or type a manual topic.
5. Click **Generate AI Reel**.
6. Show the animated vertical reel preview.
7. Walk through the generated scenes, voiceover, subtitles, thumbnail prompt, and B-roll prompts.
8. Click **Render MP4 Reel** and download the video file.
9. Show Instagram and LinkedIn publishing copy.
10. Open **Virality Lab** and explain predicted views, likes, shares, saves, and virality score.
11. Save sample feedback to demonstrate the learning loop.
12. Open **Agent Workflow** and show the autonomous workflow logs.
13. Open **Pitch Brief** to show problem, solution, architecture, business impact, and demo flow.

## Notes

This prototype generates a complete AI reel production package, animated preview, and downloadable MP4 video. The MP4 is rendered from the generated scene plan and subtitles. The generated B-roll prompts, voiceover script, subtitle lines, and thumbnail prompt can also be passed into video, voice, and image generation tools such as Runway, Veo, ElevenLabs, or other media APIs.

## Future Enhancements

- Text-to-speech voiceover export
- Auto-generated subtitle files
- AI thumbnail image generation
- Direct publishing scheduler
- Engagement feedback loop persistence
- Model-based trend learning from historical performance
