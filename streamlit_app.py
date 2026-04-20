# app.py

from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


EMBED_ID = "b88248cc-18a9-4bbc-be9e-a88dbe4f2aaf"
ANYTHINGLLM_HOST = "http://localhost:3001"
EMBED_SCRIPT_URL = f"{ANYTHINGLLM_HOST}/embed/anythingllm-chat-widget.min.js"
EMBED_API_URL = f"{ANYTHINGLLM_HOST}/api/embed"


st.set_page_config(
    page_title="Naturalborne",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


def image_to_base64(path: str) -> str:
    file_path = Path(path)
    if not file_path.exists():
        return ""
    return base64.b64encode(file_path.read_bytes()).decode("utf-8")


def build_embed_html(height: int) -> str:
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <style>
    :root {{
      color-scheme: dark;
    }}

    * {{
      box-sizing: border-box;
    }}

    html, body {{
      margin: 0;
      padding: 0;
      width: 100%;
      height: 100%;
      min-height: {height}px;
      background: #020617;
      overflow: hidden;
      font-family: Arial, Helvetica, sans-serif;
    }}

    body {{
      display: flex;
      align-items: stretch;
      justify-content: stretch;
    }}

    #mount {{
      position: relative;
      width: 100%;
      height: 100%;
      min-height: {height}px;
      background:
        radial-gradient(circle at top left, rgba(59,130,246,0.10), transparent 22%),
        linear-gradient(180deg, #020617 0%, #0b1220 100%);
      border-radius: 18px;
      overflow: hidden;
    }}

    #status {{
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 28px;
      text-align: center;
      color: #cbd5e1;
      line-height: 1.7;
      font-size: 14px;
      background: rgba(2, 6, 23, 0.72);
      z-index: 1;
    }}

    #status.hidden {{
      display: none;
    }}

    .status-card {{
      max-width: 720px;
      padding: 24px;
      border: 1px solid rgba(148, 163, 184, 0.18);
      border-radius: 18px;
      background: rgba(15, 23, 42, 0.92);
      box-shadow: 0 18px 50px rgba(0, 0, 0, 0.28);
    }}

    .status-title {{
      font-size: 18px;
      font-weight: 700;
      color: #f8fafc;
      margin-bottom: 10px;
    }}

    .status-text {{
      margin-bottom: 12px;
    }}

    .status-code {{
      display: inline-block;
      padding: 8px 12px;
      border-radius: 10px;
      background: rgba(30, 41, 59, 0.95);
      color: #93c5fd;
      word-break: break-all;
      margin: 6px 0;
    }}

    .status-list {{
      margin: 14px 0 0 0;
      padding-left: 18px;
      text-align: left;
    }}

    .status-list li {{
      margin-bottom: 8px;
    }}
  </style>
</head>
<body>
  <div id="mount">
    <div id="status">
      <div class="status-card">
        <div class="status-title">Loading Naturalborne chat</div>
        <div class="status-text">Trying to load the AnythingLLM widget from your local server.</div>
        <div class="status-code">{EMBED_SCRIPT_URL}</div>
      </div>
    </div>
  </div>

  <script>
    (function () {{
      const status = document.getElementById("status");

      function showError(message) {{
        status.classList.remove("hidden");
        status.innerHTML = `
          <div class="status-card">
            <div class="status-title">Chat widget did not load</div>
            <div class="status-text">${{message}}</div>
            <ul class="status-list">
              <li>Make sure AnythingLLM is running on port 3001.</li>
              <li>Open <span class="status-code">{EMBED_SCRIPT_URL}</span> in your browser.</li>
              <li>If your Streamlit page is HTTPS, loading HTTP localhost content may be blocked.</li>
              <li>Try opening the chat service directly in another tab.</li>
            </ul>
          </div>
        `;
      }}

      const script = document.createElement("script");
      script.src = "{EMBED_SCRIPT_URL}";
      script.async = true;

      script.setAttribute("data-embed-id", "{EMBED_ID}");
      script.setAttribute("data-base-api-url", "{EMBED_API_URL}");
      script.setAttribute("data-open-on-load", "on");
      script.setAttribute("data-position", "bottom-right");
      script.setAttribute("data-window-width", "100%");
      script.setAttribute("data-window-height", "{max(height - 40, 500)}px");
      script.setAttribute("data-assistant-name", "Naturalborne");
      script.setAttribute("data-send-message-text", "Ask a calculus question...");
      script.setAttribute("data-no-sponsor", "");
      script.setAttribute("data-no-header", "");

      script.onload = function () {{
        setTimeout(function () {{
          status.classList.add("hidden");
        }}, 1200);
      }};

      script.onerror = function () {{
        showError("The AnythingLLM embed script could not be fetched.");
      }};

      document.body.appendChild(script);

      setTimeout(function () {{
        if (!document.querySelector("anythingllm-chat-widget")) {{
          showError("The script loaded or partially loaded, but no visible widget was mounted inside this Streamlit iframe.");
        }}
      }}, 4000);
    }})();
  </script>
</body>
</html>
"""


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
    st.link_button("Open AnythingLLM", ANYTHINGLLM_HOST, use_container_width=True)
    st.link_button("Open Embed Script", EMBED_SCRIPT_URL, use_container_width=True)

height = 980 if large_chat else 780
glow = (
    "0 0 0 1px rgba(96,165,250,0.12), 0 30px 90px rgba(37,99,235,0.20)"
    if accent_glow
    else "0 18px 60px rgba(0,0,0,0.22)"
)

st.markdown(
    f"""
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
        margin-top: 16px;
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
""",
    unsafe_allow_html=True,
)

logo_html = f'<img src="data:image/png;base64,{logo_b64}" alt="Naturalborne logo">' if logo_b64 else ""

st.markdown(
    f"""
<div class="nb-hero">
    <div class="nb-brand">
        <div class="nb-logo-wrap">{logo_html}</div>
        <div>
            <h1 class="nb-title">Naturalborne</h1>
            <div class="nb-sub">
                An advanced student-focused calculus workspace for guided problem solving,
                concept support, exam assistance, and cleaner mathematical discussion in one place.
            </div>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

left, right = st.columns([1.55, 1])

with left:
    st.markdown(
        """
    <div class="nb-card">
        <div class="nb-card-title">Workspace</div>
        <div class="nb-card-text">
            Use the embedded Naturalborne chat below to ask calculus questions naturally.
            If the local widget cannot mount inside Streamlit, use the sidebar buttons to open AnythingLLM directly.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        f"""
    <div class="nb-card">
        <div class="nb-card-title">Current setup</div>
        <div class="nb-card-text">
            {'Expanded chat height is enabled.' if large_chat else 'Compact chat height is enabled.'}
            {' Extra accent glow is enabled.' if accent_glow else ' Accent glow is reduced.'}
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

if show_prompts:
    st.markdown(
        '<div class="nb-prompt-title">Suggested ways to use Naturalborne</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
    <div class="nb-prompt-wrap">
        <span class="nb-prompt">Differentiate step by step</span>
        <span class="nb-prompt">Explain a concept simply</span>
        <span class="nb-prompt">Solve in exam format</span>
        <span class="nb-prompt">Check my working</span>
        <span class="nb-prompt">Teach it like a tutor</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

if show_tips:
    st.markdown(
        """
    <div class="nb-card" style="margin-top:16px; margin-bottom:16px;">
        <div class="nb-card-title">Study tips</div>
        <div class="nb-note">
            Ask full questions for better help, include your own working when you want corrections,
            and say when you want a shorter answer or an exam-style format.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="nb-widget-shell"><div class="nb-widget-inner">', unsafe_allow_html=True)
components.html(build_embed_html(height), height=height, scrolling=False)
st.markdown("</div></div>", unsafe_allow_html=True)

st.info(
    "If the embedded widget still does not appear, open AnythingLLM directly from the sidebar. "
    "That confirms whether the issue is Streamlit iframe embedding versus the AnythingLLM server itself."
)
