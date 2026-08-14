import os
import streamlit as st
from typing import Callable

# ------------------------------------------------------------------
# PAGE CONFIG — must be the very first Streamlit call
# ------------------------------------------------------------------
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# Import the pipeline AFTER page config, wrapped in try/except so
# any missing package / bad import shows as a clear on-page error
# instead of an empty / blank app.
# ------------------------------------------------------------------
IMPORT_ERROR = None
try:
    from pipeline import run_research_pipeline
except Exception as e:
    IMPORT_ERROR = e

# ------------------------------------------------------------------
# Minimal, SAFE custom CSS — only styles a single scoped class
# (.hero). No global selectors, no backdrop-filter, no full-page
# background overrides that could break rendering.
# ------------------------------------------------------------------
st.markdown(
    """
    <style>
        .hero {
            padding: 1.8rem 2rem;
            border-radius: 16px;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
            margin-bottom: 1.5rem;
        }
        .hero h1 {
            color: #ffffff !important;
            font-size: 2rem;
            font-weight: 800;
            margin: 0;
        }
        .hero p {
            color: #f3f0ff !important;
            font-size: 1rem;
            margin-top: 0.4rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# HERO BANNER
# ------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🧠 AI Research Assistant</h1>
        <p>Search → Read → Write → Critique — a 4-agent pipeline that researches any topic for you.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# STOP EARLY IF IMPORT FAILED
# ------------------------------------------------------------------
if IMPORT_ERROR is not None:
    st.error(
        "**Could not import `run_research_pipeline` from pipeline.py**\n\n"
        f"Error: `{IMPORT_ERROR}`\n\n"
        "Checklist:\n"
        "- Is `app.py` in the SAME folder as `pipeline.py`, `agents.py`, `tools.py`, and `.env`?\n"
        "- Did you run `pip install -r requirements.txt`?\n"
        "- Is your `.env` file named exactly `.env` (not `user.env`)?"
    )
    st.stop()

# ------------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []
if "result" not in st.session_state:
    st.session_state.result = None
if "current_topic" not in st.session_state:
    st.session_state.current_topic = ""

# ------------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧠 Research Assistant")
    st.caption("Multi-agent pipeline powered by LangChain + Mistral + Tavily")

    st.divider()
    st.markdown("#### How it works")
    st.markdown(
        "1. 🔎 **Search Agent** — finds recent sources (Tavily)\n"
        "2. 📖 **Reader Agent** — scrapes the top result\n"
        "3. ✍️ **Writer** — drafts a structured report\n"
        "4. 🧐 **Critic** — reviews it and scores it"
    )

    st.divider()
    st.markdown("#### API keys")
    mistral_ok = bool(os.getenv("MISTRAL_API_KEY"))
    tavily_ok = bool(os.getenv("TAVILY_API_KEY"))
    st.markdown(f"- MISTRAL_API_KEY: {'✅ found' if mistral_ok else '❌ missing'}")
    st.markdown(f"- TAVILY_API_KEY: {'✅ found' if tavily_ok else '❌ missing'}")
    if not (mistral_ok and tavily_ok):
        st.warning("Add missing keys to your `.env` file and restart the app.")

    st.divider()
    st.markdown("#### Recent topics")
    if st.session_state.history:
        for t in reversed(st.session_state.history[-8:]):
            st.markdown(f"- {t}")
    else:
        st.caption("No topics researched yet.")

# ------------------------------------------------------------------
# INPUT
# ------------------------------------------------------------------
col1, col2 = st.columns([5, 1])
with col1:
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Impact of quantum computing on cybersecurity",
        label_visibility="collapsed",
    )
with col2:
    run_clicked = st.button("🚀 Research", use_container_width=True)

# ------------------------------------------------------------------
# RUN PIPELINE
# ------------------------------------------------------------------
if run_clicked:
    if not topic or not topic.strip():
        st.warning("Please enter a topic to research.")
    else:
        clean_topic = topic.strip()
        st.session_state.current_topic = clean_topic
        if clean_topic not in st.session_state.history:
            st.session_state.history.append(clean_topic)

        with st.spinner("Running the research pipeline... this can take a minute or two."):
            try:
                result = run_research_pipeline(clean_topic)
                st.session_state.result = result
                st.success("Pipeline complete!")
            except Exception as e:
                st.session_state.result = None
                st.error(f"Pipeline failed while running:\n\n```\n{e}\n```")

# ------------------------------------------------------------------
# RESULTS — using native st.container(border=True) instead of raw
# HTML cards, so nothing can break rendering.
# ------------------------------------------------------------------
if st.session_state.result:
    result = st.session_state.result

    st.subheader("📊 Results")
    st.caption(f"Topic: **{st.session_state.current_topic}**")

    tab_report, tab_critique, tab_search, tab_scraped = st.tabs(
        ["📝 Report", "🧐 Critique", "🔎 Search Results", "📖 Scraped Content"]
    )

    with tab_report:
        with st.container(border=True):
            st.markdown("**✍️ Writer Output**")
            st.markdown(result.get("report", "No report generated."))
        st.download_button(
            "⬇️ Download report (.md)",
            data=str(result.get("report", "")),
            file_name=f"{st.session_state.current_topic.replace(' ', '_')}_report.md",
            mime="text/markdown",
        )

    with tab_critique:
        with st.container(border=True):
            st.markdown("**🧐 Critic Feedback**")
            st.markdown(result.get("feedback", "No feedback generated."))

    with tab_search:
        with st.container(border=True):
            st.markdown("**🔎 Raw Search Results**")
            st.markdown(result.get("search_results", "No search results."))

    with tab_scraped:
        with st.container(border=True):
            st.markdown("**📖 Scraped Content**")
            st.markdown(result.get("scraped_content", "No scraped content."))
else:
    st.info("👋 Enter a topic above and click **Research** to get started.")