import html
import json

import streamlit as st
import streamlit.components.v1 as components

from content_generator import generate_reel_video_package
from trend_finder import TRACK_2_TOPICS, get_trending_topics
from virality_scorer import calculate_virality_score
from video_renderer import generate_reel_mp4


st.set_page_config(page_title="Ratefluencer Reel Agent", page_icon="R", layout="wide")


def esc(value):
    return html.escape(str(value))


def add_agent_log(message):
    st.session_state.setdefault("agent_logs", [])
    if st.session_state.agent_logs and st.session_state.agent_logs[-1] == message:
        return
    st.session_state.agent_logs.append(message)


def valid_topics(topics):
    return [topic for topic in topics if topic.get("score", 0) > 0]


def render_reel_preview(package):
    scenes = package.get("scenes", [])[:4]
    if not scenes:
        return

    scene_markup = ""
    total = max(len(scenes), 1)
    for index, scene in enumerate(scenes):
        delay = index * 3
        scene_markup += f"""
        <div class="scene" style="animation-delay:{delay}s">
            <div class="time">{esc(scene.get("time", ""))}</div>
            <div class="caption">{esc(scene.get("on_screen_text", ""))}</div>
            <div class="visual">{esc(scene.get("visual", ""))}</div>
            <div class="subtitle">{esc(scene.get("voiceover", ""))}</div>
        </div>
        """

    duration = total * 3
    components.html(f"""
    <html>
    <head>
    <style>
    body {{
        margin:0;
        background:#07070f;
        font-family:Arial, sans-serif;
    }}
    .phone {{
        width:315px;
        height:560px;
        margin:0 auto;
        position:relative;
        overflow:hidden;
        border-radius:28px;
        border:1px solid rgba(255,255,255,.16);
        background:
            radial-gradient(circle at 20% 15%, rgba(20,184,166,.45), transparent 28%),
            radial-gradient(circle at 80% 70%, rgba(245,158,11,.32), transparent 30%),
            linear-gradient(155deg, #101827, #07111f 48%, #111827);
        box-shadow:0 24px 80px rgba(0,0,0,.48);
    }}
    .scan {{
        position:absolute;
        inset:0;
        background:linear-gradient(180deg, transparent, rgba(255,255,255,.08), transparent);
        animation:scan {duration}s linear infinite;
    }}
    .brand {{
        position:absolute;
        top:18px;
        left:18px;
        right:18px;
        color:#a7f3d0;
        font-size:11px;
        letter-spacing:2px;
        text-transform:uppercase;
        z-index:5;
    }}
    .scene {{
        position:absolute;
        inset:0;
        opacity:0;
        padding:54px 22px 24px;
        box-sizing:border-box;
        animation:show {duration}s infinite;
    }}
    .time {{
        display:inline-block;
        color:#07111f;
        background:#67e8f9;
        border-radius:999px;
        padding:5px 10px;
        font-size:11px;
        font-weight:700;
    }}
    .caption {{
        margin-top:42px;
        color:white;
        font-size:34px;
        line-height:1.02;
        font-weight:900;
        letter-spacing:0;
        text-wrap:balance;
        text-shadow:0 3px 18px rgba(0,0,0,.48);
    }}
    .visual {{
        position:absolute;
        left:22px;
        right:22px;
        bottom:118px;
        color:#cbd5e1;
        font-size:13px;
        line-height:1.5;
        background:rgba(15,23,42,.7);
        border:1px solid rgba(148,163,184,.24);
        border-radius:14px;
        padding:12px;
    }}
    .subtitle {{
        position:absolute;
        left:18px;
        right:18px;
        bottom:24px;
        color:#f8fafc;
        font-size:15px;
        line-height:1.35;
        font-weight:700;
        text-align:center;
        text-shadow:0 2px 12px rgba(0,0,0,.8);
    }}
    @keyframes show {{
        0%, 100% {{ opacity:0; transform:scale(1.02); }}
        4%, 22% {{ opacity:1; transform:scale(1); }}
        26% {{ opacity:0; transform:scale(.98); }}
    }}
    @keyframes scan {{
        0% {{ transform:translateY(-100%); }}
        100% {{ transform:translateY(100%); }}
    }}
    </style>
    </head>
    <body>
        <div class="phone">
            <div class="brand">Ratefluencer AI Reel Preview</div>
            {scene_markup}
            <div class="scan"></div>
        </div>
    </body>
    </html>
    """, height=590)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500;700&display=swap');
* { font-family:'DM Sans', sans-serif; }
.stApp { background:#07070f; color:#e8e8f0; }
#MainMenu, footer, header { visibility:hidden; }
.hero {
    background:linear-gradient(135deg,#07111f 0%,#10231d 50%,#111827 100%);
    border:1px solid rgba(20,184,166,.34);
    border-radius:18px;
    padding:40px 38px;
    margin-bottom:26px;
}
.hero-title {
    font-family:'Syne',sans-serif;
    font-size:3rem;
    line-height:1.06;
    font-weight:800;
    color:#f8fafc;
    margin:0;
}
.hero-sub { color:#94a3b8; font-size:1.04rem; line-height:1.7; margin-top:12px; max-width:880px; }
.badge {
    display:inline-block;
    background:rgba(20,184,166,.12);
    border:1px solid rgba(20,184,166,.35);
    color:#67e8f9;
    padding:5px 15px;
    border-radius:999px;
    font-size:.78rem;
    font-weight:700;
    margin:4px 6px 0 0;
}
.card {
    background:linear-gradient(135deg,#0f0f1e,#111827);
    border:1px solid rgba(148,163,184,.14);
    border-radius:12px;
    padding:22px;
    margin-bottom:16px;
}
.card-label {
    font-family:'Syne',sans-serif;
    font-size:.7rem;
    font-weight:800;
    color:#38bdf8;
    letter-spacing:2.2px;
    text-transform:uppercase;
    margin-bottom:7px;
}
.card-title {
    font-family:'Syne',sans-serif;
    font-size:1.25rem;
    font-weight:800;
    color:#f0f9ff;
    margin-bottom:14px;
}
.content-box {
    background:#0c0c1a;
    border:1px solid rgba(255,255,255,.07);
    border-radius:10px;
    padding:18px;
    font-size:.92rem;
    line-height:1.72;
    color:#cbd5e1;
    white-space:pre-wrap;
    margin-bottom:12px;
}
.metric-box {
    background:#0f0f1e;
    border:1px solid rgba(255,255,255,.07);
    border-radius:10px;
    padding:16px;
    text-align:center;
}
.metric-val { font-family:'Syne',sans-serif; font-size:1.55rem; font-weight:800; color:#67e8f9; }
.metric-lbl { color:#64748b; font-size:.72rem; text-transform:uppercase; letter-spacing:1.4px; margin-top:4px; }
.trend-row {
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:12px;
    background:#0f0f1e;
    border:1px solid rgba(255,255,255,.06);
    border-radius:10px;
    padding:12px 18px;
    margin-bottom:8px;
}
.trend-title { color:#e2e8f0; font-size:.9rem; font-weight:600; flex:1; }
.trend-score { font-family:'Syne',sans-serif; font-size:1rem; font-weight:800; color:#67e8f9; }
.trend-meta { color:#94a3b8; font-size:.8rem; font-weight:600; }
.section-label {
    font-family:'Syne',sans-serif;
    font-size:.72rem;
    font-weight:800;
    color:#38bdf8;
    letter-spacing:2.2px;
    text-transform:uppercase;
    margin-bottom:10px;
}
.prog-wrap { margin-bottom:10px; }
.prog-label { display:flex; justify-content:space-between; color:#94a3b8; font-size:.8rem; margin-bottom:4px; }
.prog-bar { background:#1e293b; border-radius:99px; height:8px; overflow:hidden; }
.prog-fill { height:100%; border-radius:99px; background:linear-gradient(90deg,#14b8a6,#38bdf8,#f59e0b); }
.score-big { font-family:'Syne',sans-serif; font-size:4.8rem; font-weight:800; line-height:1; color:#67e8f9; }
.agent-step { display:flex; align-items:flex-start; gap:14px; padding:12px 0; border-bottom:1px solid rgba(255,255,255,.05); }
.agent-icon { color:#22c55e; font-weight:800; margin-top:2px; }
.agent-text { color:#94a3b8; font-size:.88rem; line-height:1.5; }
.agent-text strong { color:#67e8f9; }
.stButton>button, .stDownloadButton>button {
    background:linear-gradient(135deg,#0f766e,#1d4ed8) !important;
    color:white !important;
    border:none !important;
    border-radius:10px !important;
    padding:12px 24px !important;
    font-family:'Syne',sans-serif !important;
    font-weight:800 !important;
}
[data-testid="stSidebar"] { background:#080812 !important; border-right:1px solid rgba(56,189,248,.15) !important; }
hr { border-color:rgba(56,189,248,.12) !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-title">AI Viral Reel Creator Agent</div>
    <div class="hero-sub">Track 2 prototype for discovering trends, ranking topics, generating a 30-60 second reel, producing voiceover, subtitles, thumbnail and B-roll prompts, publishing captions, and predicting virality before posting.</div>
    <div style="margin-top:16px">
        <span class="badge">Trend Discovery</span>
        <span class="badge">AI Reel Generator</span>
        <span class="badge">Voiceover + Subtitles</span>
        <span class="badge">Virality Prediction</span>
    </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""<div style="text-align:center;padding:18px 0 8px">
        <div style="font-family:Syne;font-size:1.1rem;font-weight:800;color:#f8fafc;">RATEFLUENCER</div>
        <div style="color:#475569;font-size:.72rem;margin-top:4px;letter-spacing:2px;">TRACK 2 REEL AGENT</div>
    </div>""", unsafe_allow_html=True)
    st.divider()
    page = st.radio(
        "Navigation",
        ["Reel Generator", "Trend Discovery", "Virality Lab", "Agent Workflow", "Pitch Brief"],
        label_visibility="collapsed",
    )
    st.divider()
    category = st.selectbox("Trend Category", list(TRACK_2_TOPICS.keys()))
    audience = st.text_input("Target Audience", "creators and marketers")
    tone = st.selectbox("Reel Tone", ["high-energy", "educational", "contrarian", "founder-style", "professional"])


if page == "Reel Generator":
    topics = get_trending_topics(category)
    live_topics = valid_topics(topics)
    add_agent_log(f"Trend Discovery Agent scanned {category}")

    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        (len(live_topics), "Ranked Trends"),
        ("30-60s", "Reel Length"),
        ("4", "Video Scenes"),
        ("0-100", "Virality Score"),
    ]
    for col, (value, label) in zip([c1, c2, c3, c4], metrics):
        col.markdown(f'<div class="metric-box"><div class="metric-val">{esc(value)}</div><div class="metric-lbl">{esc(label)}</div></div>', unsafe_allow_html=True)

    st.divider()
    left, right = st.columns([1.05, .95])
    with left:
        st.markdown('<div class="section-label">Select Topic</div>', unsafe_allow_html=True)
        if live_topics:
            options = [topic["title"] for topic in live_topics]
            selected_topic = st.selectbox("Trending topic", options)
            selected_meta = next((topic for topic in live_topics if topic["title"] == selected_topic), {})
            st.caption(f"Source: {selected_meta.get('source', 'Unknown')} | Trend Score: {selected_meta.get('score', 0)} | Confidence: {selected_meta.get('confidence', 0)}")
        else:
            st.warning("Live trend data unavailable. Enter a verified topic manually for demo generation.")
            selected_topic = st.text_input("Manual topic", "AI agents for creator marketing")

        generate = st.button("Generate AI Reel", use_container_width=True)
    with right:
        st.markdown("""
        <div class="card">
            <div class="card-label">Track 2 Workflow</div>
            <div class="card-title">What the agent creates</div>
            <div style="color:#94a3b8;line-height:1.8;">
                Hook and 30-60 second story<br>
                Voiceover script for TTS<br>
                Captions and subtitles<br>
                Thumbnail concept<br>
                B-roll and visual prompts<br>
                Instagram and LinkedIn publishing copy
            </div>
        </div>
        """, unsafe_allow_html=True)

    if generate and selected_topic:
        with st.spinner("Generating reel scenes, voiceover, subtitles, B-roll prompts, and publishing copy..."):
            package = generate_reel_video_package(selected_topic, audience, tone)
            st.session_state.reel_package = package
            st.session_state.selected_topic = selected_topic
            add_agent_log("Script Generation Agent produced reel structure")
            add_agent_log("Automated Reel Generator produced voiceover, subtitles, thumbnail, and B-roll prompts")
            add_agent_log("Publishing Agent produced Instagram and LinkedIn copy")
        st.success("AI reel package generated.")

    if "reel_package" in st.session_state:
        package = st.session_state.reel_package
        st.divider()
        preview_col, detail_col = st.columns([.9, 1.1])
        with preview_col:
            st.markdown('<div class="section-label">AI Video Preview</div>', unsafe_allow_html=True)
            render_reel_preview(package)
            score, breakdown = calculate_virality_score(st.session_state.selected_topic, package.get("voiceover_script", ""))
            st.session_state.virality_score = score
            st.session_state.virality_breakdown = breakdown
            add_agent_log("Virality Prediction Engine scored generated reel")
            label = "High Viral Potential" if score >= 75 else "Good Potential" if score >= 50 else "Needs stronger packaging"
            st.markdown(f"""<div class="card" style="text-align:center;">
                <div class="score-big">{score}</div>
                <div style="color:#64748b;font-size:.72rem;letter-spacing:3px;text-transform:uppercase;margin:8px 0;">Virality Score</div>
                <div style="background:rgba(20,184,166,.1);border-radius:8px;padding:8px 14px;color:#67e8f9;font-size:.78rem;font-weight:700;">{esc(label)}</div>
            </div>""", unsafe_allow_html=True)

        with detail_col:
            st.markdown('<div class="section-label">Reel Package</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="content-box"><strong>{esc(package.get("title", "Generated Reel"))}</strong><br><br><strong>Hook:</strong> {esc(package.get("hook", ""))}<br><br><strong>Voiceover:</strong><br>{esc(package.get("voiceover_script", ""))}</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-label">Scene-by-Scene Video Plan</div>', unsafe_allow_html=True)
            for index, scene in enumerate(package.get("scenes", []), 1):
                st.markdown(f"""<div class="content-box"><strong>Scene {index} - {esc(scene.get("time", ""))}</strong>
Visual: {esc(scene.get("visual", ""))}
On-screen text: {esc(scene.get("on_screen_text", ""))}
Voiceover: {esc(scene.get("voiceover", ""))}
B-roll prompt: {esc(scene.get("broll_prompt", ""))}</div>""", unsafe_allow_html=True)

            st.download_button(
                "Download Reel Package JSON",
                data=json.dumps(package, indent=2),
                file_name="ratefluencer_reel_package.json",
                mime="application/json",
                use_container_width=True,
            )

            render_mp4 = st.button("Render MP4 Reel", use_container_width=True)
            if render_mp4:
                try:
                    with st.spinner("Rendering vertical MP4 reel from generated scenes and subtitles..."):
                        st.session_state.reel_mp4 = generate_reel_mp4(package)
                        add_agent_log("Video Rendering Agent exported downloadable MP4")
                    st.success("MP4 reel rendered.")
                except RuntimeError as error:
                    st.error(str(error))

            if "reel_mp4" in st.session_state:
                st.video(st.session_state.reel_mp4)
                st.download_button(
                    "Download Reel as MP4",
                    data=st.session_state.reel_mp4,
                    file_name="ratefluencer_ai_reel.mp4",
                    mime="video/mp4",
                    use_container_width=True,
                )

        st.divider()
        pub1, pub2, pub3 = st.columns(3)
        with pub1:
            st.markdown('<div class="section-label">Thumbnail Prompt</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="content-box">{esc(package.get("thumbnail_prompt", ""))}</div>', unsafe_allow_html=True)
        with pub2:
            st.markdown('<div class="section-label">Instagram Caption</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="content-box">{esc(package.get("instagram_caption", ""))}</div>', unsafe_allow_html=True)
        with pub3:
            st.markdown('<div class="section-label">LinkedIn Post</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="content-box">{esc(package.get("linkedin_post", ""))}</div>', unsafe_allow_html=True)


elif page == "Trend Discovery":
    st.markdown('<div class="card-label">Trend Discovery Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title" style="font-size:1.5rem;">Track 2 Trend Ranking</div>', unsafe_allow_html=True)
    topics = get_trending_topics(category)
    live_topics = valid_topics(topics)
    if not live_topics:
        st.warning("Live trend data unavailable. Configure NEWS_API_KEY to rank current trends from news platforms.")

    for index, topic in enumerate(sorted(topics, key=lambda item: item.get("score", 0), reverse=True), 1):
        rank = "-" if topic.get("score", 0) == 0 else f"#{index}"
        st.markdown(f"""<div class="trend-row">
            <div style="color:#f59e0b;font-family:Syne;font-weight:800;">{rank}</div>
            <div class="trend-title">{esc(topic.get("title", ""))}</div>
            <div class="trend-score">{topic.get("score", 0)}</div>
            <div class="trend-meta">{esc(topic.get("growth", "N/A"))}</div>
            <div class="trend-meta">{esc(topic.get("source", "Unknown"))}</div>
        </div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="section-label">Ranking Signals</div>', unsafe_allow_html=True)
    confidence = int(sum(topic.get("confidence", 0) for topic in topics) / max(len(topics), 1))
    factors = {
        "Growth Velocity": confidence,
        "Search Interest Proxy": 100 if live_topics else 0,
        "Engagement Potential": min(confidence + 8, 100),
        "Novelty": min(confidence + 3, 100),
        "Audience Relevance": min(len(live_topics) * 10, 100),
    }
    for factor, value in factors.items():
        st.markdown(f"""<div class="prog-wrap">
            <div class="prog-label"><span>{esc(factor)}</span><span>{value}/100</span></div>
            <div class="prog-bar"><div class="prog-fill" style="width:{value}%"></div></div>
        </div>""", unsafe_allow_html=True)


elif page == "Virality Lab":
    st.markdown('<div class="card-label">Virality Prediction Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title" style="font-size:1.5rem;">Predict Before Publishing</div>', unsafe_allow_html=True)
    package = st.session_state.get("reel_package")
    if not package:
        st.info("Generate a reel first to score its predicted performance.")
    else:
        score = st.session_state.get("virality_score")
        breakdown = st.session_state.get("virality_breakdown", {})
        if score is None:
            score, breakdown = calculate_virality_score(st.session_state.get("selected_topic", ""), package.get("voiceover_script", ""))
        estimates = {
            "Expected Views": score * 1400,
            "Expected Likes": score * 310,
            "Expected Shares": score * 82,
            "Expected Saves": score * 120,
        }
        cols = st.columns(4)
        for col, (label, value) in zip(cols, estimates.items()):
            col.markdown(f'<div class="metric-box"><div class="metric-val">{value:,}</div><div class="metric-lbl">{esc(label)}</div></div>', unsafe_allow_html=True)
        st.divider()
        for factor, value in breakdown.items():
            max_value = {"Hook Strength": 20, "Content Depth": 20, "Trend Alignment": 20, "Emotional Trigger": 15, "CTA Strength": 15, "Platform Fit": 10}.get(factor, 20)
            pct = int((value / max_value) * 100)
            st.markdown(f"""<div class="prog-wrap">
                <div class="prog-label"><span>{esc(factor)}</span><span>{value}/{max_value}</span></div>
                <div class="prog-bar"><div class="prog-fill" style="width:{pct}%"></div></div>
            </div>""", unsafe_allow_html=True)

        st.divider()
        st.markdown('<div class="section-label">Learning Loop</div>', unsafe_allow_html=True)
        with st.form("performance_feedback"):
            f1, f2, f3, f4 = st.columns(4)
            with f1:
                actual_views = st.number_input("Actual views", min_value=0, value=0, step=100)
            with f2:
                actual_likes = st.number_input("Actual likes", min_value=0, value=0, step=10)
            with f3:
                actual_shares = st.number_input("Actual shares", min_value=0, value=0, step=5)
            with f4:
                actual_saves = st.number_input("Actual saves", min_value=0, value=0, step=5)
            saved_feedback = st.form_submit_button("Save Performance Feedback")

        if saved_feedback:
            st.session_state.performance_feedback = {
                "views": actual_views,
                "likes": actual_likes,
                "shares": actual_shares,
                "saves": actual_saves,
                "topic": st.session_state.get("selected_topic", ""),
            }
            add_agent_log("Learning Loop captured post-publish engagement signals")
            st.success("Performance feedback saved for future recommendation tuning.")

        if "performance_feedback" in st.session_state:
            feedback = st.session_state.performance_feedback
            engagement_actions = feedback["likes"] + feedback["shares"] + feedback["saves"]
            engagement_rate = round((engagement_actions / max(feedback["views"], 1)) * 100, 2)
            st.markdown(f'<div class="content-box">Saved feedback for {esc(feedback["topic"])}. Engagement action rate: {engagement_rate}%. The agent can use this signal to tune future hooks, CTAs, and platform-fit recommendations.</div>', unsafe_allow_html=True)


elif page == "Agent Workflow":
    st.markdown('<div class="card-label">Autonomous AI Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title" style="font-size:1.5rem;">AI Reel Creation Workflow</div>', unsafe_allow_html=True)
    workflow = [
        ("Trend Discovery Agent", "Discovers topic candidates across AI, technology, business, startups, finance, and creator economy."),
        ("Trend Ranking Engine", "Ranks topics with growth velocity, engagement potential, novelty, and audience relevance signals."),
        ("Script Generation Agent", "Creates hook, story, key insights, and CTA for a 30-60 second reel."),
        ("Automated Reel Generator", "Generates voiceover, captions, subtitles, thumbnail concept, B-roll prompts, and visual assets."),
        ("Video Rendering Agent", "Converts the generated scene plan into a vertical MP4 reel with subtitles."),
        ("Publishing Agent", "Creates Instagram captions, hashtags, LinkedIn posts, and engagement hooks."),
        ("Virality Prediction Engine", "Predicts views, likes, shares, saves, and total virality score before publishing."),
        ("Learning Loop", "Stores real engagement results to improve future reel recommendations."),
    ]
    for title, description in workflow:
        st.markdown(f'<div class="agent-step"><div class="agent-icon">OK</div><div class="agent-text"><strong>{esc(title)}</strong><br>{esc(description)}</div></div>', unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="section-label">Current Run Logs</div>', unsafe_allow_html=True)
    logs = st.session_state.get("agent_logs", [])
    if logs:
        for log in logs[-14:]:
            st.markdown(f'<div class="agent-step"><div class="agent-icon">OK</div><div class="agent-text">{esc(log)}</div></div>', unsafe_allow_html=True)
    else:
        st.info("Generate a reel to populate live execution logs.")


elif page == "Pitch Brief":
    st.markdown('<div class="card-label">Demo Readiness</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title" style="font-size:1.5rem;">Track 2 Submission Brief</div>', unsafe_allow_html=True)

    p1, p2 = st.columns(2)
    with p1:
        st.markdown("""
        <div class="card">
            <div class="card-label">Problem</div>
            <div class="card-title">Creators lose time before they ever publish</div>
            <div style="color:#94a3b8;line-height:1.8;">
                They manually search trends, write scripts, plan visuals, create captions, and guess whether the reel will perform.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown("""
        <div class="card">
            <div class="card-label">Solution</div>
            <div class="card-title">One agent creates the complete reel package</div>
            <div style="color:#94a3b8;line-height:1.8;">
                The app discovers a trend, generates the reel, exports MP4, prepares publishing copy, and predicts virality.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">System Architecture</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="content-box">NewsAPI / Manual Topic -> Trend Ranking Engine -> Groq LLaMA Reel Generator -> Structured Reel Package -> MP4 Rendering Agent -> Publishing Assets -> Virality Prediction -> Performance Learning Loop</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Business Impact</div>', unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown('<div class="metric-box"><div class="metric-val">10x</div><div class="metric-lbl">Faster Content Planning</div></div>', unsafe_allow_html=True)
    with b2:
        st.markdown('<div class="metric-box"><div class="metric-val">1</div><div class="metric-lbl">Trend To Reel Workflow</div></div>', unsafe_allow_html=True)
    with b3:
        st.markdown('<div class="metric-box"><div class="metric-val">MP4</div><div class="metric-lbl">Ready Demo Output</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">Demo Flow</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="content-box">1. Select a Track 2 trend category.
2. Pick a live topic or enter a manual topic.
3. Generate the AI reel package.
4. Show the animated preview and scene plan.
5. Render and download the MP4.
6. Show Instagram and LinkedIn publishing copy.
7. Open Virality Lab to explain predicted views, likes, shares, and saves.
8. Save feedback in the learning loop.</div>
    """, unsafe_allow_html=True)


st.markdown('<div style="text-align:center;color:#334155;font-size:.78rem;padding:30px 0 10px;">Ratefluencer AI Hackathon 2026 - Track 2: AI Viral Reel Creator Agent</div>', unsafe_allow_html=True)
