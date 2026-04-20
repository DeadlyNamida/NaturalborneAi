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


def build_embed_html(min_height: int) -> str:
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta
    name="viewport"
    content="width=device-width, initial-scale=1.0, maximum-scale=1.0"
  />
  <style>
    * {{
      box-sizing: border-box;
    }}

    html, body {{
      margin: 0;
      padding: 0;
      width: 100%;
      min-height: {min_height}px;
      background: transparent;
      overflow: hidden;
      font-family: Arial, Helvetica, sans-serif;
    }}

    body {{
      position: relative;
    }}

    #mount {{
      position: relative;
      width: 100%;
      min-height: {min_height}px;
      background: transparent;
      overflow: visible;
    }}
  </style>
</head>
<body>
  <div id="mount"></div>

  <script>
    (function () {{
      const MIN_HEIGHT = {min_height};

      function getDocumentHeight() {{
        const body = document.body;
        const html = document.documentElement;
        return Math.max(
          body.scrollHeight,
          body.offsetHeight,
          html.clientHeight,
          html.scrollHeight,
          html.offsetHeight,
          MIN_HEIGHT
        );
      }}

      function sendHeight() {{
        const height = getDocumentHeight();
        window.parent.postMessage(
          {{
            type: "anythingllm-embed-height",
            height: height
          }},
          "*"
        );
      }}

      const script = document.createElement("script");
      script.src = "{EMBED_SCRIPT_URL}";
      script.async = true;
      script.setAttribute("data-embed-id", "{EMBED_ID}");
      script.setAttribute("data-base-api-url", "{EMBED_API_URL}");
      script.setAttribute("data-open-on-load", "on");
      script.setAttribute("data-window-width", "100%");
      script.setAttribute("data-window-height", "{min_height}px");
      script.setAttribute("data-assistant-name", "Naturalborne");
      script.setAttribute("data-send-message-text", "Ask a calculus question...");
      script.setAttribute("data-no-sponsor", "");
      script.setAttribute("data-no-header", "");

      script.onload = function () {{
        sendHeight();
        setTimeout(sendHeight, 250);
        setTimeout(sendHeight, 750);
        setTimeout(sendHeight, 1500);
        setTimeout(sendHeight, 3000);
      }};

      document.body.appendChild(script);

      const observer = new ResizeObserver(function () {{
        sendHeight();
      }});

      observer.observe(document.documentElement);
      observer.observe(document.body);

      window.addEventListener("load", sendHeight);
      window.addEventListener("resize", sendHeight);

      const intervalId = setInterval(sendHeight, 1000);
      window.addEventListener("beforeunload", function () {{
        clearInterval(intervalId);
        observer.disconnect();
      }});
    }})();
  </script>
</body>
</html>
"""


logo_b64 = image_to_base64("logo.png")

with st.sidebar:
    st.markdown("## Naturalborne")
    st.caption("Advanced Calculus Workspace")
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

glow = (
    "0 0 0 1px rgba(96,165,250,0.12), 0 30px 90px rgba(37,99,235,0.20)"
    if accent_glow
    else "0 18px 60px rgba(0,0,0,0.22)"
)

min_chat_height = 640

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
        max-width: 1380px;
        padding-top: 2.2rem;
        padding-bottom: 1.2rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
    }}

    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(15,23,42,0.98), rgba(17,24,39,0.98));
        border-right: 1px solid rgba(148,163,184,0.10);
    }}

    [data-testid="stSidebar"] .block-container {{
        padding-top: 1.4rem;
    }}

    .nb-hero {{
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, rgba(15,23,42,0.94), rgba(17,24,39,0.90));
        border: 1px solid rgba(148,163,184,0.12);
        border-radius: 30px;
        padding: 1.4rem 1.5rem 1.25rem;
        margin-bottom: 0.75rem;
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
        width: 80px;
        height: 80px;
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
        width: 56px;
        height: 56px;
        object-fit: contain;
        display: block;
    }}

    .nb-title {{
        margin: 0;
        font-size: 2.55rem;
        line-height: 1;
        font-weight: 800;
        letter-spacing: -0.04em;
        color: #f8fafc;
    }}

    .nb-sub {{
        margin-top: 0.45rem;
        color: #cbd5e1;
        max-width: 900px;
        line-height: 1.65;
        font-size: 0.98rem;
    }}

    .nb-card {{
        background: rgba(15,23,42,0.74);
        border: 1px solid rgba(148,163,184,0.12);
        border-radius: 24px;
        padding: 1rem 1.1rem;
        box-shadow: 0 14px 38px rgba(0,0,0,0.16);
    }}

    .nb-card-title {{
        color: #93c5fd;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 0.78rem;
        font-weight: 700;
        margin-bottom: 0.45rem;
    }}

    .nb-card-text {{
        color: #dbe3ef;
        font-size: 0.96rem;
        line-height: 1.65;
    }}

    .nb-widget-shell {{
        position: relative;
        background:
            radial-gradient(circle at top left, rgba(59,130,246,0.10), transparent 24%),
            radial-gradient(circle at bottom right, rgba(14,165,233,0.08), transparent 22%),
            rgba(7,12,24,0.64);
        border: 1px solid rgba(148,163,184,0.12);
        border-radius: 28px;
        padding: 0;
        box-shadow: {glow};
        overflow: hidden;
        margin-top: 10px;
    }}

    .nb-widget-inner {{
        margin-top: 0;
        padding-top: 0;
        border-radius: 22px;
        overflow: hidden;
        background: transparent;
        min-height: {min_chat_height}px;
    }}

    .nb-prompt-title {{
        font-size: 1.2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0 0 0.6rem 0;
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

    .nb-resize-script {{
        display: none;
    }}

    @media (max-width: 950px) {{
        .block-container {{
            padding-top: 1.6rem;
            padding-left: 0.9rem;
            padding-right: 0.9rem;
        }}

        .nb-brand {{
            align-items: flex-start;
        }}

        .nb-title {{
            font-size: 2.1rem;
        }}

        .nb-hero {{
            padding: 1.2rem;
        }}

        .nb-widget-inner {{
            min-height: 560px;
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
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        """
        <div class="nb-card">
            <div class="nb-card-title">Live chat</div>
            <div class="nb-card-text">
                Auto-resizing embedded AnythingLLM workspace.
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
        <div class="nb-card" style="margin-top:14px; margin-bottom:12px;">
            <div class="nb-card-title">Study tips</div>
            <div class="nb-note">
                Ask full questions for better help, include your own working when you want corrections,
                and say when you want a shorter answer or an exam-style format.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <script class="nb-resize-script">
      (function () {
        if (window.__anythingllmResizeListenerInstalled) return;
        window.__anythingllmResizeListenerInstalled = true;

        function resizeAnythingLLMIframes() {
          const iframes = window.parent.document.querySelectorAll('iframe[title="st.iframe"], iframe');
          for (const iframe of iframes) {
            try {
              const srcdoc = iframe.getAttribute("srcdoc") || "";
              if (srcdoc.includes("anythingllm-embed-height") || srcdoc.includes("anythingllm-chat-widget")) {
                iframe.style.height = window.__anythingllmLastHeight || "640px";
              }
            } catch (error) {}
          }
        }

        window.addEventListener("message", function (event) {
          const data = event.data;
          if (!data || data.type !== "anythingllm-embed-height") return;

          const nextHeight = Math.max(Number(data.height || 0), 640);
          window.__anythingllmLastHeight = `${nextHeight}px`;

          const iframes = window.parent.document.querySelectorAll('iframe[title="st.iframe"], iframe');
          for (const iframe of iframes) {
            try {
              const srcdoc = iframe.getAttribute("srcdoc") || "";
              if (srcdoc.includes("anythingllm-embed-height") || srcdoc.includes("anythingllm-chat-widget")) {
                iframe.style.height = `${nextHeight}px`;
              }
            } catch (error) {}
          }
        });

        setInterval(resizeAnythingLLMIframes, 1000);
      })();
    </script>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="nb-widget-shell"><div class="nb-widget-inner">', unsafe_allow_html=True)
components.html(build_embed_html(min_chat_height), height=min_chat_height, scrolling=False)
st.markdown("</div></div>", unsafe_allow_html=True)
