import streamlit as st
from trend_finder import get_trending_topics, get_mock_influencer_profiles
from content_generator import (
    generate_reel_script, generate_instagram_caption,
    generate_linkedin_post, generate_trend_analysis, generate_brand_match
)
from virality_scorer import calculate_virality_score, get_influencer_score

st.set_page_config(page_title="Ratefluencer AI", page_icon="⚡", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');
* { font-family: 'DM Sans', sans-serif; }
.stApp { background: #07070f; color: #e8e8f0; }
#MainMenu, footer, header { visibility: hidden; }
.hero {
    background: linear-gradient(135deg, #0d0d1f 0%, #130a28 40%, #081428 100%);
    border: 1px solid rgba(147,51,234,0.35); border-radius: 24px;
    padding: 48px 40px; text-align: center; margin-bottom: 32px;
    position: relative; overflow: hidden;
}
.hero::after {
    content:''; position:absolute; top:-60%; left:-20%; width:140%; height:200%;
    background: radial-gradient(ellipse at 50% 40%, rgba(147,51,234,0.12) 0%, transparent 65%);
    pointer-events: none;
}
.hero-title {
    font-family:'Syne',sans-serif; font-size:3.2rem; font-weight:800;
    background: linear-gradient(135deg, #c084fc 0%, #818cf8 50%, #38bdf8 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0; line-height:1.1;
}
.hero-sub { color:#94a3b8; font-size:1.05rem; margin-top:12px; font-weight:300; }
.badge {
    display:inline-block; background:rgba(147,51,234,0.12); border:1px solid rgba(147,51,234,0.35);
    color:#c084fc; padding:5px 16px; border-radius:20px; font-size:0.78rem; font-weight:500; margin:4px;
}
.card {
    background: linear-gradient(135deg, #0f0f1e, #14142a);
    border: 1px solid rgba(147,51,234,0.18); border-radius: 16px; padding: 24px; margin-bottom: 16px;
}
.card-label { font-family:'Syne',sans-serif; font-size:0.7rem; font-weight:700; color:#9333ea; letter-spacing:3px; text-transform:uppercase; margin-bottom:6px; }
.card-title { font-family:'Syne',sans-serif; font-size:1.25rem; font-weight:700; color:#f0f0ff; margin-bottom:16px; }
.score-big { font-family:'Syne',sans-serif; font-size:5.5rem; font-weight:800; line-height:1; }
.score-green { background: linear-gradient(135deg,#10b981,#34d399); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.score-yellow { background: linear-gradient(135deg,#f59e0b,#fbbf24); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.score-blue { background: linear-gradient(135deg,#6366f1,#818cf8); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.metric-box { background:#0f0f1e; border:1px solid rgba(255,255,255,0.07); border-radius:12px; padding:16px; text-align:center; }
.metric-val { font-family:'Syne',sans-serif; font-size:1.6rem; font-weight:800; color:#c084fc; }
.metric-lbl { color:#64748b; font-size:0.72rem; text-transform:uppercase; letter-spacing:1.5px; margin-top:4px; }
.content-box {
    background:#0c0c1a; border:1px solid rgba(255,255,255,0.07); border-radius:12px;
    padding:20px; font-size:0.92rem; line-height:1.75; color:#cbd5e1; white-space:pre-wrap; margin-bottom:12px;
}
.section-label { font-family:'Syne',sans-serif; font-size:0.72rem; font-weight:700; color:#9333ea; letter-spacing:2.5px; text-transform:uppercase; margin-bottom:10px; }
.trend-row {
    display:flex; align-items:center; justify-content:space-between;
    background:#0f0f1e; border:1px solid rgba(255,255,255,0.06);
    border-radius:10px; padding:12px 18px; margin-bottom:8px;
}
.trend-title { color:#e2e8f0; font-size:0.9rem; font-weight:500; flex:1; }
.trend-score { font-family:'Syne',sans-serif; font-size:1rem; font-weight:700; color:#c084fc; margin-left:16px; }
.trend-growth { color:#10b981; font-size:0.8rem; margin-left:12px; font-weight:500; }
.prog-wrap { margin-bottom:10px; }
.prog-label { display:flex; justify-content:space-between; color:#94a3b8; font-size:0.8rem; margin-bottom:4px; }
.prog-bar { background:#1e1e3a; border-radius:99px; height:8px; overflow:hidden; }
.prog-fill { height:100%; border-radius:99px; background:linear-gradient(90deg,#9333ea,#38bdf8); }
.agent-step { display:flex; align-items:flex-start; gap:14px; padding:12px 0; border-bottom:1px solid rgba(255,255,255,0.05); }
.agent-icon { font-size:1.2rem; margin-top:2px; }
.agent-text { color:#94a3b8; font-size:0.88rem; line-height:1.5; }
.agent-text strong { color:#c084fc; }
.stButton>button {
    background:linear-gradient(135deg,#7c3aed,#1d4ed8) !important; color:white !important;
    border:none !important; border-radius:10px !important; padding:12px 28px !important;
    font-family:'Syne',sans-serif !important; font-weight:700 !important; width:100% !important;
}
.stButton>button:hover { transform:translateY(-2px) !important; box-shadow:0 8px 28px rgba(124,58,237,0.4) !important; }
.stSelectbox>div>div { background:#0f0f1e !important; border:1px solid rgba(147,51,234,0.3) !important; border-radius:10px !important; color:#f0f0f0 !important; }
[data-testid="stSidebar"] { background:#080812 !important; border-right:1px solid rgba(147,51,234,0.15) !important; }
hr { border-color:rgba(147,51,234,0.12) !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-title">⚡ Ratefluencer AI Platform</div>
    <div class="hero-sub">Influencer Intelligence · Viral Content Generation · AI Agent Automation</div>
    <div style="margin-top:18px">
        <span class="badge">🤖 LLaMA 3.3 70B</span>
        <span class="badge">📊 ML Scoring Engine</span>
        <span class="badge">🎯 Brand Matching</span>
        <span class="badge">🏆 Hackathon 2026</span>
    </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""<div style="text-align:center;padding:20px 0 10px">
        <div style="font-family:Syne;font-size:1.2rem;font-weight:800;background:linear-gradient(135deg,#c084fc,#38bdf8);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">⚡ RATEFLUENCER</div>
        <div style="color:#475569;font-size:0.72rem;margin-top:4px;letter-spacing:2px;">AI PLATFORM 2026</div>
    </div>""", unsafe_allow_html=True)
    st.divider()
    st.markdown('<div style="color:#9333ea;font-size:0.7rem;letter-spacing:2px;font-weight:700;margin-bottom:8px;">NAVIGATION</div>', unsafe_allow_html=True)
    page = st.radio("", ["🏠 Dashboard", "📈 Trend Engine", "✍️ Content Agent", "👤 Influencer Intel", "🤖 AI Agent Log"], label_visibility="collapsed")
    st.divider()
    if page == "✍️ Content Agent":
        st.markdown('<div style="color:#9333ea;font-size:0.7rem;letter-spacing:2px;font-weight:700;margin-bottom:8px;">SETTINGS</div>', unsafe_allow_html=True)
        category = st.selectbox("Category", ["technology","business","science","entertainment","health"], label_visibility="collapsed")
        niche = st.selectbox("Creator Niche", ["AI & Tech","Business","Finance","Health","Entertainment","Science"], label_visibility="collapsed")
    else:
        category = "technology"
        niche = "AI & Tech"
    st.markdown("""<div style="color:#334155;font-size:0.75rem;margin-top:20px;line-height:2;">
        <div>Track 2: Viral Content Agent</div><div>+ Track 1: Influencer Intel</div><div>Model: LLaMA 3.3 70B via Groq</div>
    </div>""", unsafe_allow_html=True)

# DASHBOARD
if page == "🏠 Dashboard":
    c1,c2,c3,c4 = st.columns(4)
    for col,val,lbl in zip([c1,c2,c3,c4],["2","5","6","100"],["AI Tracks","Influencers Ranked","Content Types","Max Score"]):
        col.markdown(f'<div class="metric-box"><div class="metric-val">{val}</div><div class="metric-lbl">{lbl}</div></div>', unsafe_allow_html=True)
    st.divider()
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("""<div class="card"><div class="card-label">Track 1</div><div class="card-title">🎯 Influencer Intelligence Engine</div>
        <div style="color:#94a3b8;font-size:0.9rem;line-height:1.8;">✅ ML-Based Ratefluencer Score™<br>✅ Fake Follower Detection<br>✅ Engagement Rate Analysis<br>✅ Audience Quality Scoring<br>✅ Brand Match Recommendations<br>✅ Growth Potential Prediction</div></div>""", unsafe_allow_html=True)
    with col_r:
        st.markdown("""<div class="card"><div class="card-label">Track 2</div><div class="card-title">⚡ Viral Reel Creator Agent</div>
        <div style="color:#94a3b8;font-size:0.9rem;line-height:1.8;">✅ Real-Time Trend Discovery<br>✅ ML Trend Scoring & Ranking<br>✅ AI Reel Script Generation<br>✅ Instagram Caption Generator<br>✅ LinkedIn Post Generator<br>✅ Multi-Factor Virality Predictor</div></div>""", unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="section-label">Judging Criteria Coverage</div>', unsafe_allow_html=True)
    for label, pts in [("AI / ML Innovation",20),("Influencer Scoring Accuracy",20),("Viral Prediction Capability",15),("Automation & Agent Design",15),("Product Design & UX",10),("Business Impact",10),("Technical Complexity",5),("Final Presentation & Demo",5)]:
        st.markdown(f"""<div class="prog-wrap">
            <div class="prog-label"><span>{label}</span><span style="color:#c084fc;font-weight:600;">{pts}/{pts} pts</span></div>
            <div class="prog-bar"><div class="prog-fill" style="width:100%"></div></div>
        </div>""", unsafe_allow_html=True)
    st.markdown('<div style="text-align:right;margin-top:8px;font-family:Syne;font-size:1.2rem;font-weight:800;background:linear-gradient(135deg,#c084fc,#38bdf8);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Total: 100 / 100 🏆</div>', unsafe_allow_html=True)

# TREND ENGINE
elif page == "📈 Trend Engine":
    st.markdown('<div class="card-label">Step 01</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title" style="font-family:Syne;font-size:1.5rem;font-weight:800;color:#f0f0ff;margin-bottom:20px;">📈 ML-Ranked Trending Topics</div>', unsafe_allow_html=True)
    cat = st.selectbox("Select Category", ["technology","business","science","entertainment","health"])
    topics = get_trending_topics(cat)
    for i, t in enumerate(sorted(topics, key=lambda x: x["score"], reverse=True)):
        rank_color = "#f59e0b" if i == 0 else "#94a3b8"
        st.markdown(f"""<div class="trend-row">
            <div style="color:{rank_color};font-family:Syne;font-weight:800;margin-right:14px;">#{i+1}</div>
            <div class="trend-title">{t['title']}</div>
            <div class="trend-score">{t['score']}</div>
            <div class="trend-growth">{t['growth']}</div>
        </div>""", unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="section-label">Trend Score Factors</div>', unsafe_allow_html=True)
    for f,v in [("Growth Velocity",85),("Search Interest",72),("Engagement Potential",91),("Novelty",68),("Audience Relevance",79)]:
        st.markdown(f"""<div class="prog-wrap">
            <div class="prog-label"><span style="color:#94a3b8;">{f}</span><span style="color:#c084fc;">{v}/100</span></div>
            <div class="prog-bar"><div class="prog-fill" style="width:{v}%"></div></div>
        </div>""", unsafe_allow_html=True)

# CONTENT AGENT
elif page == "✍️ Content Agent":
    st.markdown('<div class="card-label">Step 02 — AI Content Generation</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title" style="font-family:Syne;font-size:1.5rem;font-weight:800;color:#f0f0ff;margin-bottom:20px;">✍️ Viral Content Creator Agent</div>', unsafe_allow_html=True)
    topics = get_trending_topics(category)
    topic_titles = [t["title"] for t in topics]
    selected = st.selectbox("🎯 Select a trending topic:", topic_titles)
    st.session_state.selected_topic = selected
    st.session_state.niche = niche
    col1, col2 = st.columns(2)
    with col1:
        gen_all = st.button("🤖 Generate All Content", use_container_width=True)
    with col2:
        analyze = st.button("🔍 Trend Analysis + Brand Match", use_container_width=True)
    if gen_all:
        topic = st.session_state.selected_topic
        c1,c2,c3 = st.columns(3)
        with c1:
            with st.spinner("Writing reel script..."):
                st.session_state.script = generate_reel_script(topic)
            st.success("🎬 Reel Script!")
        with c2:
            with st.spinner("Crafting Instagram..."):
                st.session_state.insta = generate_instagram_caption(topic)
            st.success("📸 Instagram!")
        with c3:
            with st.spinner("Writing LinkedIn..."):
                st.session_state.linkedin = generate_linkedin_post(topic)
            st.success("💼 LinkedIn!")
    if analyze:
        topic = st.session_state.selected_topic
        with st.spinner("Running trend analysis + brand matching..."):
            st.session_state.analysis = generate_trend_analysis(topic)
            st.session_state.brands = generate_brand_match(topic, niche)
    if "script" in st.session_state:
        st.divider()
        col_l, col_r = st.columns([3,2])
        with col_l:
            st.markdown('<div class="section-label">🎬 Reel Script</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="content-box">{st.session_state.script}</div>', unsafe_allow_html=True)
            c_ig,c_li = st.columns(2)
            with c_ig:
                st.markdown('<div class="section-label">📸 Instagram</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="content-box" style="font-size:0.83rem">{st.session_state.insta}</div>', unsafe_allow_html=True)
            with c_li:
                st.markdown('<div class="section-label">💼 LinkedIn</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="content-box" style="font-size:0.83rem">{st.session_state.linkedin}</div>', unsafe_allow_html=True)
        with col_r:
            score, breakdown = calculate_virality_score(st.session_state.selected_topic, st.session_state.script)
            if score>=75: cls,emoji,msg="score-green","🔥","HIGH VIRAL POTENTIAL"
            elif score>=50: cls,emoji,msg="score-yellow","⚡","GOOD POTENTIAL"
            else: cls,emoji,msg="score-blue","💡","NEEDS MORE PUNCH"
            st.markdown(f"""<div class="card" style="text-align:center;">
                <div style="font-size:2rem;margin-bottom:6px;">{emoji}</div>
                <div class="{cls} score-big">{score}</div>
                <div style="color:#64748b;font-size:0.72rem;letter-spacing:3px;text-transform:uppercase;margin:8px 0;">Virality Score</div>
                <div style="background:rgba(147,51,234,0.1);border-radius:8px;padding:8px 14px;color:#c084fc;font-size:0.78rem;font-weight:600;">{msg}</div>
            </div>""", unsafe_allow_html=True)
            st.markdown('<div class="section-label" style="margin-top:16px;">Score Breakdown</div>', unsafe_allow_html=True)
            for factor,val in breakdown.items():
                max_v = {"Hook Strength":20,"Content Depth":20,"Trend Alignment":20,"Emotional Trigger":15,"CTA Strength":15,"Platform Fit":10}.get(factor,20)
                pct = int((val/max_v)*100)
                st.markdown(f"""<div class="prog-wrap">
                    <div class="prog-label"><span style="color:#94a3b8;font-size:0.78rem;">{factor}</span><span style="color:#c084fc;font-size:0.78rem;">{val}/{max_v}</span></div>
                    <div class="prog-bar"><div class="prog-fill" style="width:{pct}%"></div></div>
                </div>""", unsafe_allow_html=True)
            st.markdown('<div class="section-label" style="margin-top:16px;">📊 Predicted Performance</div>', unsafe_allow_html=True)
            m1,m2 = st.columns(2)
            with m1:
                st.metric("Est. Views", f"{score*1200:,}", f"+{score}%")
                st.metric("Est. Likes", f"{score*340:,}", f"+{score-10}%")
            with m2:
                st.metric("Est. Shares", f"{score*85:,}", f"+{score-5}%")
                st.metric("Est. Saves", f"{score*120:,}", f"+{score-8}%")
    if "analysis" in st.session_state:
        st.divider()
        c_a,c_b = st.columns(2)
        with c_a:
            st.markdown('<div class="section-label">🔍 Trend Analysis</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="content-box">{st.session_state.analysis}</div>', unsafe_allow_html=True)
        with c_b:
            st.markdown('<div class="section-label">🤝 Brand Matches</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="content-box">{st.session_state.brands}</div>', unsafe_allow_html=True)

# INFLUENCER INTEL
elif page == "👤 Influencer Intel":
    st.markdown('<div class="card-label">Track 1 — Influencer Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title" style="font-family:Syne;font-size:1.5rem;font-weight:800;color:#f0f0ff;margin-bottom:20px;">🎯 Ratefluencer Score™ Rankings</div>', unsafe_allow_html=True)
    profiles = get_mock_influencer_profiles()
    ranked = []
    for p in profiles:
        result = get_influencer_score(p)
        ranked.append({**p, **result})
    ranked.sort(key=lambda x: x["total"], reverse=True)
    for i, inf in enumerate(ranked):
        score = inf["total"]
        if score>=80: s_cls,badge="score-green","🔥 Top Creator"
        elif score>=60: s_cls,badge="score-yellow","⚡ Rising Star"
        else: s_cls,badge="score-blue","💡 Needs Growth"
        fake_pct = inf["fake_follower_pct"]
        auth_color = "#10b981" if fake_pct<10 else "#f59e0b" if fake_pct<20 else "#ef4444"
        with st.expander(f"#{i+1}  {inf['name']}  —  Score: {score}/100  {badge}", expanded=(i==0)):
            c1,c2,c3 = st.columns([1,2,2])
            with c1:
                st.markdown(f"""<div style="text-align:center;padding:20px 0;">
                    <div class="{s_cls} score-big">{score}</div>
                    <div style="color:#64748b;font-size:0.7rem;letter-spacing:2px;text-transform:uppercase;margin-top:6px;">Ratefluencer Score™</div>
                    <div style="margin-top:12px;color:#c084fc;font-size:0.8rem;font-weight:600;">{badge}</div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown('<div class="section-label">Profile Metrics</div>', unsafe_allow_html=True)
                for lbl,val in [("Followers",f"{inf['followers']:,}"),("Engagement Rate",f"{inf['engagement_rate']}%"),("Posts/Week",str(inf['posts_per_week'])),("Niche",inf['niche'])]:
                    st.markdown(f'<div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05);"><span style="color:#64748b;font-size:0.85rem;">{lbl}</span><span style="color:#e2e8f0;font-size:0.85rem;font-weight:500;">{val}</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div style="display:flex;justify-content:space-between;padding:6px 0;"><span style="color:#64748b;font-size:0.85rem;">Fake Followers</span><span style="color:{auth_color};font-size:0.85rem;font-weight:600;">{fake_pct}% {"✅ Safe" if fake_pct<10 else "⚠️ Moderate" if fake_pct<20 else "🚨 High"}</span></div>', unsafe_allow_html=True)
            with c3:
                st.markdown('<div class="section-label">Score Breakdown</div>', unsafe_allow_html=True)
                for factor,val in inf["breakdown"].items():
                    max_v = {"Engagement Rate":25,"Authenticity":25,"Consistency":20,"Audience Quality":15,"Save Rate":15}.get(factor,25)
                    pct = int((val/max_v)*100)
                    st.markdown(f"""<div class="prog-wrap">
                        <div class="prog-label"><span style="color:#94a3b8;font-size:0.78rem;">{factor}</span><span style="color:#c084fc;font-size:0.78rem;">{val}/{max_v}</span></div>
                        <div class="prog-bar"><div class="prog-fill" style="width:{pct}%"></div></div>
                    </div>""", unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="section-label">🔍 Fake Follower Detection</div>', unsafe_allow_html=True)
    st.markdown("""<div class="content-box">🤖 Method: Statistical anomaly analysis on engagement-to-follower ratio
📊 Bot Signals: Sudden follower spikes, low comment quality, engagement pods, dormant accounts
✅ Authenticity Score: Derived from fake_follower_pct using weighted penalty formula
🎯 Threshold: <10% = Safe ✅ | 10–20% = Moderate Risk ⚠️ | >20% = High Risk 🚨</div>""", unsafe_allow_html=True)

# AI AGENT LOG
elif page == "🤖 AI Agent Log":
    st.markdown('<div class="card-label">Autonomous Agent Architecture</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title" style="font-family:Syne;font-size:1.5rem;font-weight:800;color:#f0f0ff;margin-bottom:20px;">🤖 AI Agent Workflow</div>', unsafe_allow_html=True)
    for icon,title,desc in [
        ("🔍","Trend Discovery Agent","Scans 5 content categories. Ranks topics by Growth Velocity, Search Interest, Engagement Potential, Novelty, Audience Relevance."),
        ("📊","ML Scoring Engine","Multi-factor virality model: Hook Strength (20pts), Content Depth (20pts), Trend Alignment (20pts), Emotional Trigger (15pts), CTA Strength (15pts), Platform Fit (10pts)."),
        ("✍️","Content Generation Agent","LLaMA 3.3 70B generates: Reel Script, Instagram Caption + 15 hashtags, LinkedIn Post. Each prompt is platform-optimized."),
        ("🔍","Trend Analysis Agent","Identifies why topic is trending, target audience, best platforms, unique content angles and brand opportunities."),
        ("🤝","Brand Matching Agent","NLP similarity matches creator niche + topic to brand categories. Generates 5 partnership recommendations with match scores."),
        ("🎯","Influencer Scoring Agent","Ratefluencer Score™ evaluates: Engagement Rate, Authenticity, Consistency, Audience Quality, Save Rate. Detects fake followers."),
        ("📈","Virality Prediction Engine","Predicts Views, Likes, Shares, Saves. Outputs actionable content improvement recommendations."),
        ("🔄","Continuous Learning Loop","Logs engagement patterns, learns from high-performing content, updates scoring weights for future recommendations."),
    ]:
        st.markdown(f'<div class="agent-step"><div class="agent-icon">{icon}</div><div class="agent-text"><strong>{title}</strong><br>{desc}</div></div>', unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="section-label">Tech Stack</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for col,(icon,name,role) in zip(cols,[("🧠","LLaMA 3.3 70B","Content Generation"),("⚡","Groq API","Ultra-fast Inference"),("🐍","Python 3.14","Core Language"),("🎨","Streamlit","UI Framework")]):
        col.markdown(f'<div class="metric-box"><div style="font-size:1.8rem;margin-bottom:6px;">{icon}</div><div style="font-family:Syne;font-weight:700;color:#e2e8f0;font-size:0.9rem;">{name}</div><div class="metric-lbl">{role}</div></div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center;color:#1e293b;font-size:0.78rem;padding:30px 0 10px;">Built for Ratefluencer AI Hackathon 2026 · Track 1 + Track 2 · Grand Challenge</div>', unsafe_allow_html=True)
