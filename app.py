import streamlit as st
from trend_finder import get_trending_topics
from content_generator import generate_reel_script, generate_instagram_caption, generate_linkedin_post
from virality_scorer import calculate_virality_score

# Page config
st.set_page_config(
    page_title="Ratefluencer AI Agent",
    page_icon="🚀",
    layout="wide"
)

# Header
st.title("🚀 Ratefluencer AI Viral Content Agent")
st.subheader("Discover Trends → Generate Scripts → Predict Virality")
st.divider()

# Sidebar
st.sidebar.title("⚙️ Settings")
category = st.sidebar.selectbox(
    "Select Trend Category",
    ["technology", "business", "science", "entertainment", "health"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("Built for Ratefluencer AI Hackathon 2026 🏆")

# Step 1: Trend Discovery
st.header("📈 Step 1: Trending Topics")

if st.button("🔍 Fetch Trending Topics", use_container_width=True):
    with st.spinner("Fetching latest trends..."):
        topics = get_trending_topics(category)
        st.session_state.topics = topics

if "topics" in st.session_state:
    topics = st.session_state.topics
    
    if topics:
        st.success(f"Found {len(topics)} trending topics!")
        
        topic_titles = [t["title"] for t in topics if t["title"]]
        selected_topic = st.selectbox("Select a topic to create content:", topic_titles)
        st.session_state.selected_topic = selected_topic
    else:
        st.error("No topics found. Check your NewsAPI key.")

st.divider()

# Step 2: Content Generation
st.header("✍️ Step 2: AI Content Generation")

if "selected_topic" in st.session_state:
    st.info(f"**Selected Topic:** {st.session_state.selected_topic}")
    
    if st.button("🤖 Generate All Content", use_container_width=True):
        topic = st.session_state.selected_topic
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            with st.spinner("Generating Reel Script..."):
                script = generate_reel_script(topic)
                st.session_state.script = script
            st.success("✅ Reel Script Ready!")
        
        with col2:
            with st.spinner("Generating Instagram Caption..."):
                insta = generate_instagram_caption(topic)
                st.session_state.insta = insta
            st.success("✅ Instagram Caption Ready!")
        
        with col3:
            with st.spinner("Generating LinkedIn Post..."):
                linkedin = generate_linkedin_post(topic)
                st.session_state.linkedin = linkedin
            st.success("✅ LinkedIn Post Ready!")

st.divider()

# Step 3: Show Results
st.header("📋 Step 3: Your Content")

if "script" in st.session_state:
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎬 Reel Script")
        st.text_area("", st.session_state.script, height=300)
        
        st.subheader("📸 Instagram Caption")
        st.text_area("", st.session_state.insta, height=200)
    
    with col2:
        st.subheader("💼 LinkedIn Post")
        st.text_area("", st.session_state.linkedin, height=200)
        
        # Virality Score
        st.subheader("🔥 Virality Score")
        score = calculate_virality_score(
            st.session_state.selected_topic,
            st.session_state.script
        )
        
        st.session_state.score = score
        
        if score >= 75:
            st.success(f"🔥 Virality Score: {score}/100 — High Viral Potential!")
        elif score >= 50:
            st.warning(f"⚡ Virality Score: {score}/100 — Good Potential!")
        else:
            st.info(f"💡 Virality Score: {score}/100 — Needs More punch!")
        
        st.progress(score / 100)
        