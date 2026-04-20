import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64

st.set_page_config(page_title="Naturalborne", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

def image_to_base64(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return ""
    return base64.b64encode(p.read_bytes()).decode("utf-8")

logo_b64 = image_to_base64("logo.png")

with st.sidebar:
    st.markdown("## Naturalborne")
    st.caption("Advanced Calculus Workspace")
    large_chat = st.toggle("Large chat area", value=True)
    show_tips = st.toggle("Show study tips", value=True)
    show_prompts = st.toggle("Show prompt ideas", value=True)
    accent_glow = st.toggle("Accent glow", value=True)

    st.markdown("---")
    st.markdown("### Modes")
    st.markdown("- Step by step")
    st.markdown("- Exam assistance")
    st.markdown("- Concept tutoring")
    st.markdown("- Error checking")

    st.markdown("---")
    st.caption("Make sure AnythingLLM is running on port 3001.")

height = 980 if large_chat else 780
glow = "0 0 0 1px rgba(96,165,250,0.12), 0 30px 90px rgba(37,99,235,0.20)" if accent_glow else "0 18px 60px rgba(0,0,0,0.22)"

st.markdown(f"""
<style>
    .stApp {{
        background:
            radial-gradient(circle at top left, rgba(59,130,246,0.14), transparent 26%),
            radial-gradient(circle at bottom right, rgba(14,165,233,0.10), transparent 20%),
            linear-gradient(180deg, #020617 0%, #0b1220 48%, #0b1120 100%);
        color: #f8fafc;
    }}

    .block-container {{
        max-width: 1280px;
        padding-top: 3.8rem;
        padding-bottom: 2rem;
        padding-left: 1.4rem;
        padding-right: 1.4rem;
    }}

    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(15,23,42,0.98), rgba(17,24,39,0.98));
        border-right: 1px solid rgba(148,163,184,0.10);
    }}

    [data-testid="stSidebar"] .block-container {{
        padding-top: 1.6rem;
    }}

    .nb-hero {{
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, rgba(15,23,42,0.94), rgba(17,24,39,0.90));
        border: 1px solid rgba(148,163,184,0.12);
        border-radius: 30px;
        padding: 2rem 2rem 1.8rem;
        margin-bottom: 1rem;
        box-shadow: {glow};
    }}

    .nb-hero::before {{
        content: "";
        position: absolute;
        inset: -20% auto auto -10%;
        width: 280px;
        height: 280px;
        background: radial-gradient(circle, rgba(37,99,235,0.18), transparent 70%);
        pointer-events: none;
    }}

    .nb-brand {{
        display: flex;
        align-items: center;
        gap: 18px;
        position: relative;
        z-index: 2;
    }}

    .nb-logo-wrap {{
        width: 86px;
        height: 86px;
        border-radius: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(15,23,42,0.74);
        border: 1px solid rgba(96,165,250,0.14);
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
        flex-shrink: 0;
    }}

    .nb-logo-wrap img {{
        width: 58px;
        height: 58px;
        object-fit: contain;
        display: block;
    }}

    .nb-title {{
        margin: 0;
        font-size: 3rem;
        line-height: 1;
        font-weight: 800;
        letter-spacing: -0.04em;
        color: #f8fafc;
    }}

    .nb-sub {{
        margin-top: 0.6rem;
        color: #cbd5e1;
        max-width: 860px;
        line-height: 1.8;
        font-size: 1.03rem;
    }}

    .nb-chip-row {{
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 1rem;
        position: relative;
        z-index: 2;
    }}

    .nb-chip {{
        display: inline-flex;
        align-items: center;
        padding: 0.56rem 0.88rem;
        border-radius: 999px;
        background: rgba(37,99,235,0.14);
        border: 1px solid rgba(96,165,250,0.22);
        color: #dbeafe;
        font-size: 0.88rem;
    }}

    .nb-grid {{
        display: grid;
        grid-template-columns: 1.6fr 1fr;
        gap: 16px;
        margin-bottom: 1rem;
    }}

    .nb-card {{
        background: rgba(15,23,42,0.74);
        border: 1px solid rgba(148,163,184,0.12);
        border-radius: 24px;
        padding: 1.15rem 1.15rem;
        box-shadow: 0 14px 38px rgba(0,0,0,0.16);
    }}

    .nb-card-title {{
        color: #93c5fd;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 0.78rem;
        font-weight: 700;
        margin-bottom: 0.55rem;
    }}

    .nb-card-text {{
        color: #dbe3ef;
        font-size: 0.98rem;
        line-height: 1.7;
    }}

    .nb-widget-shell {{
        position: relative;
        background: rgba(7,12,24,0.64);
        border: 1px solid rgba(148,163,184,0.12);
        border-radius: 28px;
        padding: 18px;
        box-shadow: {glow};
        overflow: hidden;
    }}

    .nb-widget-shell::before {{
        content: "Naturalborne Live Workspace";
        position: absolute;
        top: 14px;
        left: 18px;
        color: #93c5fd;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 0.74rem;
        font-weight: 700;
        z-index: 2;
        pointer-events: none;
    }}

    .nb-widget-inner {{
        margin-top: 26px;
        border-radius: 22px;
        overflow: hidden;
        background: rgba(2,6,23,0.5);
        min-height: 560px;
    }}

    .nb-prompt-title {{
        font-size: 1.4rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0 0 0.7rem 0;
        color: #f8fafc;
    }}

    .nb-prompt-wrap {{
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }}

    .nb-prompt {{
        display: inline-flex;
        padding: 0.8rem 1rem;
        border-radius: 999px;
        background: linear-gradient(135deg, rgba(37,99,235,0.94), rgba(29,78,216,0.90));
        color: white;
        font-weight: 700;
        font-size: 0.9rem;
        box-shadow: 0 10px 28px rgba(37,99,235,0.18);
    }}

    .nb-note {{
        color: #a9bbd3;
        line-height: 1.7;
        font-size: 0.96rem;
    }}

    @media (max-width: 950px) {{
        .block-container {{
            padding-top: 3rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }}
        .nb-grid {{
            grid-template-columns: 1fr;
        }}
        .nb-brand {{
            align-items: flex-start;
        }}
        .nb-title {{
            font-size: 2.3rem;
        }}
        .nb-hero {{
            padding: 1.35rem;
        }}
    }}
</style>
""", unsafe_allow_html=True)

logo_html = f'<img src="data:image/png;base64,{logo_b64}" alt="Naturalborne logo">' if logo_b64 else ""

st.markdown(f"""
<div class="nb-hero">
    <div class="nb-brand">
        <div class="nb-logo-wrap">{logo_html}</div>
        <div>
            <h1 class="nb-title">Naturalborne</h1>
            <div class="nb-sub">
                An advanced student-focused calculus workspace for guided problem solving, concept support,
                exam assistance, and cleaner mathematical discussion in one place.
            </div>
        </div>
    </div>

    <div class="nb-chip-row">
        <span class="nb-chip">Step by step</span>
        <span class="nb-chip">Exam assistance</span>
        <span class="nb-chip">Concept tutoring</span>
        <span class="nb-chip">Error checking</span>
        <span class="nb-chip">Modern workspace</span>
    </div>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1.55, 1])

with left:
    st.markdown("""
    <div class="nb-card">
        <div class="nb-card-title">Workspace</div>
        <div class="nb-card-text">
            Use the embedded Naturalborne chat below to ask calculus questions naturally.
            The layout is designed to feel cleaner, more focused, and more like a polished final project interface.
        </div>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div class="nb-card">
        <div class="nb-card-title">Current setup</div>
        <div class="nb-card-text">
            {'Expanded chat height is enabled.' if large_chat else 'Compact chat height is enabled.'}
            {' Extra accent glow is enabled.' if accent_glow else ' Accent glow is reduced.'}
        </div>
    </div>
    """, unsafe_allow_html=True)

if show_prompts:
    st.markdown('<div class="nb-prompt-title">Suggested ways to use Naturalborne</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="nb-prompt-wrap">
        <span class="nb-prompt">Differentiate step by step</span>
        <span class="nb-prompt">Explain a concept simply</span>
        <span class="nb-prompt">Solve in exam format</span>
        <span class="nb-prompt">Check my working</span>
        <span class="nb-prompt">Teach it like a tutor</span>
    </div>
    """, unsafe_allow_html=True)

if show_tips:
    st.markdown("""
    <div class="nb-card" style="margin-top:16px; margin-bottom:16px;">
        <div class="nb-card-title">Study tips</div>
        <div class="nb-note">
            Ask full questions for better help, include your own working when you want corrections,
            and say when you want a shorter answer or an exam-style format.
        </div>
    </div>
    """, unsafe_allow_html=True)

embed_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<style>
html, body {
    margin: 0;
    padding: 0;
    background: transparent;
    overflow: hidden;
}
</style>
</head>
<body>
<script
  data-embed-id="b88248cc-18a9-4bbc-be9e-a88dbe4f2aaf"
  data-base-api-url="http://127.0.0.1:3001/api/embed"
  src="http://127.0.0.1:3001/embed/anythingllm-chat-widget.min.js">
</script>
</body>
</html>
"""

st.markdown('<div class="nb-widget-shell"><div class="nb-widget-inner">', unsafe_allow_html=True)
components.html(embed_html, height=height, scrolling=False)
st.markdown('</div></div>', unsafe_allow_html=True)
