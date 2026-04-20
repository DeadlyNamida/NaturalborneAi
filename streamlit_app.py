# app.py

from __future__ import annotations

import base64
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

EMBED_ID = "b88248cc-18a9-4bbc-be9e-a88dbe4f2aaf"
ANYTHINGLLM_HOST = "http://localhost:3001"
EMBED_SCRIPT_URL = f"{ANYTHINGLLM_HOST}/embed/anythingllm-chat-widget.min.js"
EMBED_API_URL = f"{ANYTHINGLLM_HOST}/api/embed"

PROMPTS = [
    "Differentiate x^3 ln(x) step by step.",
    "Integrate sin(x)^2 from 0 to pi.",
    "Explain the chain rule with a simple example.",
    "Find the derivative of e^(x^2) and explain each step.",
    "Solve this limit: lim(x→0) (sin x)/x.",
    "Use implicit differentiation on x^2 + y^2 = 25.",
    "Find critical points and classify them for f(x)=x^3-3x^2+2.",
    "Teach me u-substitution like a tutor.",
]

MODES = {
    "Step by step": "Work step by step. Show each step clearly and do not skip reasoning.",
    "Exam assistance": "Answer in exam style. Be concise, structured, and show working clearly.",
    "Concept tutoring": "Teach like a tutor. Explain the concept simply before solving.",
    "Error checking": "Check my work carefully. Point out mistakes and correct them clearly.",
}


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


def compose_prompt(base_prompt: str, mode_name: str) -> str:
    mode_text = MODES.get(mode_name, "")
    return f"{mode_text}\n\n{base_prompt}".strip()


def build_embed_html(initial_height: int, pending_prompt: str, apply_nonce: int) -> str:
    pending_prompt_json = json.dumps(pending_prompt)
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <style>
    * {{
      box-sizing: border-box;
    }}

    html, body {{
      margin: 0;
      padding: 0;
      width: 100%;
      min-height: {initial_height}px;
      background: transparent;
      overflow: hidden;
      font-family: Arial, Helvetica, sans-serif;
      color: #f8fafc;
    }}

    body {{
      position: relative;
    }}

    #mount {{
      position: relative;
      width: 100%;
      min-height: {initial_height}px;
      background: transparent;
      overflow: visible;
    }}

    #status {{
      color: rgba(203, 213, 225, 0.72);
      font-size: 14px;
      padding: 2px 0 6px 2px;
    }}

    #status.hidden {{
      display: none;
    }}
  </style>
</head>
<body>
  <div id="mount">
    <div id="status">Loading Naturalborne chat…</div>
  </div>

  <script>
    (function () {{
      const pendingPrompt = {pending_prompt_json};
      const applyNonce = {apply_nonce};
      const status = document.getElementById("status");

      function getBestHeight() {{
        const body = document.body;
        const doc = document.documentElement;
        const widget = document.querySelector("anythingllm-chat-widget");

        const values = [
          body ? body.scrollHeight : 0,
          body ? body.offsetHeight : 0,
          doc ? doc.scrollHeight : 0,
          doc ? doc.offsetHeight : 0,
          doc ? doc.clientHeight : 0,
          widget ? widget.scrollHeight : 0,
          widget ? widget.offsetHeight : 0
        ];

        return Math.max(...values, {initial_height});
      }}

      function setFrameHeight(height) {{
        const safeHeight = Math.max(height || 0, 520);
        window.parent.postMessage(
          {{
            isStreamlitMessage: true,
            type: "streamlit:setFrameHeight",
            height: safeHeight
          }},
          "*"
        );
      }}

      function resizeNow() {{
        requestAnimationFrame(() => {{
          setFrameHeight(getBestHeight());
        }});
      }}

      function deepQuerySelector(root, selectors) {{
        if (!root) return null;

        for (const selector of selectors) {{
          try {{
            const found = root.querySelector(selector);
            if (found) return found;
          }} catch (e) {{}}
        }}

        const all = root.querySelectorAll ? root.querySelectorAll("*") : [];
        for (const el of all) {{
          if (el.shadowRoot) {{
            const found = deepQuerySelector(el.shadowRoot, selectors);
            if (found) return found;
          }}
        }}

        return null;
      }}

      function deepQueryAllTextControls(root) {{
        const results = [];

        function visit(node) {{
          if (!node || !node.querySelectorAll) return;

          const local = node.querySelectorAll(
            'textarea, input[type="text"], input:not([type]), [contenteditable="true"], [role="textbox"]'
          );

          for (const el of local) {{
            results.push(el);
          }}

          const all = node.querySelectorAll("*");
          for (const el of all) {{
            if (el.shadowRoot) {{
              visit(el.shadowRoot);
            }}
          }}
        }}

        visit(root);
        return results;
      }}

      function setValueOnElement(el, text) {{
        if (!el) return false;

        try {{
          el.focus();
        }} catch (e) {{}}

        if ("value" in el) {{
          const proto = Object.getPrototypeOf(el);
          const setter = Object.getOwnPropertyDescriptor(proto, "value")?.set;

          if (setter) {{
            setter.call(el, text);
          }} else {{
            el.value = text;
          }}

          el.dispatchEvent(new Event("input", {{ bubbles: true }}));
          el.dispatchEvent(new Event("change", {{ bubbles: true }}));
          return true;
        }}

        if (el.isContentEditable) {{
          el.textContent = text;
          el.dispatchEvent(new Event("input", {{ bubbles: true }}));
          return true;
        }}

        return false;
      }}

      function findBestTextbox() {{
        const widget = document.querySelector("anythingllm-chat-widget");
        const roots = [document, widget?.shadowRoot].filter(Boolean);

        const selectors = [
          'textarea[placeholder*="Ask" i]',
          'textarea[placeholder*="message" i]',
          'textarea',
          'input[type="text"][placeholder*="Ask" i]',
          'input[type="text"][placeholder*="message" i]',
          '[contenteditable="true"]',
          '[role="textbox"]'
        ];

        for (const root of roots) {{
          const direct = deepQuerySelector(root, selectors);
          if (direct) return direct;

          const controls = deepQueryAllTextControls(root);
          if (controls.length) return controls[controls.length - 1];
        }}

        return null;
      }}

      function applyPrompt(text) {{
        if (!text) return;

        let attempts = 0;

        function tryFill() {{
          attempts += 1;
          const textbox = findBestTextbox();

          if (textbox && setValueOnElement(textbox, text)) {{
            try {{
              textbox.focus();
            }} catch (e) {{}}
            status.textContent = "Prompt inserted into the chat box.";
            status.classList.remove("hidden");
            setTimeout(() => {{
              status.classList.add("hidden");
              resizeNow();
            }}, 1200);
            return;
          }}

          if (attempts < 16) {{
            setTimeout(tryFill, 300);
          }}
        }}

        tryFill();
      }}

      const observer = new MutationObserver(() => {{
        resizeNow();

        const widget = document.querySelector("anythingllm-chat-widget");
        if (widget) {{
          status.classList.add("hidden");
        }}
      }});

      observer.observe(document.documentElement, {{
        childList: true,
        subtree: true,
        attributes: true
      }});

      window.addEventListener("load", resizeNow);
      window.addEventListener("resize", resizeNow);

      setInterval(resizeNow, 700);

      const script = document.createElement("script");
      script.src = "{EMBED_SCRIPT_URL}";
      script.async = true;
      script.setAttribute("data-embed-id", "{EMBED_ID}");
      script.setAttribute("data-base-api-url", "{EMBED_API_URL}");
      script.setAttribute("data-open-on-load", "on");
      script.setAttribute("data-window-width", "100%");
      script.setAttribute("data-window-height", "{initial_height}px");
      script.setAttribute("data-assistant-name", "Naturalborne");
      script.setAttribute("data-send-message-text", "Ask a calculus question...");
      script.setAttribute("data-no-sponsor", "");
      script.setAttribute("data-no-header", "");

      script.onload = function () {{
        setTimeout(resizeNow, 200);
        setTimeout(resizeNow, 800);
        setTimeout(() => applyPrompt(pendingPrompt), 1200);
      }};

      document.body.appendChild(script);

      if (applyNonce > 0) {{
        setTimeout(() => applyPrompt(pendingPrompt), 1600);
      }}

      resizeNow();
    }})();
  </script>
</body>
</html>
"""


if "mode" not in st.session_state:
    st.session_state.mode = "Step by step"

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = ""

if "apply_nonce" not in st.session_state:
    st.session_state.apply_nonce = 0


logo_b64 = image_to_base64("logo.png")

with st.sidebar:
    st.markdown("## Naturalborne")
    st.caption("Advanced Calculus Workspace")
    show_tips = st.toggle("Show study tips", value=True)
    accent_glow = st.toggle("Accent glow", value=True)

    st.markdown("---")
    st.caption("Make sure AnythingLLM is running on port 3001.")
    st.link_button("Open AnythingLLM", ANYTHINGLLM_HOST, use_container_width=True)

glow = (
    "0 0 0 1px rgba(96,165,250,0.12), 0 30px 90px rgba(37,99,235,0.20)"
    if accent_glow
    else "0 18px 60px rgba(0,0,0,0.22)"
)

initial_chat_height = 720

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
        padding-top: 2.0rem;
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
        padding: 1.55rem 1.6rem 1.35rem;
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
        font-size: 2.7rem;
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

    .nb-embed {{
        margin-top: 8px;
        border-radius: 22px;
        overflow: visible;
        background: transparent;
    }}

    .nb-section {{
        margin-top: 14px;
    }}

    .nb-section-title {{
        color: #f8fafc;
        font-size: 1.08rem;
        font-weight: 800;
        margin: 0 0 0.8rem 0;
        letter-spacing: -0.02em;
    }}

    .nb-mode-note {{
        color: #a9bbd3;
        font-size: 0.94rem;
        margin-top: 0.4rem;
        line-height: 1.6;
    }}

    div[data-testid="stRadio"] > label {{
        display: none;
    }}

    div[role="radiogroup"] {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
    }}

    div[role="radiogroup"] > label {{
        margin: 0;
        background: rgba(15,23,42,0.76);
        border: 1px solid rgba(148,163,184,0.14);
        border-radius: 999px;
        padding: 0.65rem 0.95rem;
    }}

    .stButton > button {{
        width: 100%;
        border-radius: 999px;
        border: 1px solid rgba(96,165,250,0.22);
        background: linear-gradient(135deg, rgba(37,99,235,0.94), rgba(29,78,216,0.90));
        color: white;
        font-weight: 700;
        padding: 0.8rem 1rem;
        box-shadow: 0 10px 28px rgba(37,99,235,0.18);
    }}

    .nb-note {{
        color: #a9bbd3;
        line-height: 1.7;
        font-size: 0.96rem;
    }}

    @media (max-width: 950px) {{
        .block-container {{
            padding-top: 1.4rem;
            padding-left: 0.9rem;
            padding-right: 0.9rem;
        }}

        .nb-brand {{
            align-items: flex-start;
        }}

        .nb-title {{
            font-size: 2.15rem;
        }}

        .nb-hero {{
            padding: 1.2rem;
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
                Use the chat first, then click a prompt below to auto-fill the text box with your chosen mode.
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
                Auto-resizing AnythingLLM embed with modes and calculus prompts underneath.
            </div>
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
                Pick a mode, click a prompt below, then edit the question in the chat box if needed.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="nb-embed">', unsafe_allow_html=True)
components.html(
    build_embed_html(
        initial_chat_height,
        st.session_state.pending_prompt,
        st.session_state.apply_nonce,
    ),
    height=initial_chat_height,
    scrolling=False,
)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="nb-section">', unsafe_allow_html=True)
st.markdown('<div class="nb-section-title">Working mode</div>', unsafe_allow_html=True)

selected_mode = st.radio(
    "Working mode",
    list(MODES.keys()),
    index=list(MODES.keys()).index(st.session_state.mode),
    horizontal=True,
    key="mode_radio",
)
st.session_state.mode = selected_mode

st.markdown(
    f'<div class="nb-mode-note">{MODES[st.session_state.mode]}</div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="nb-section-title" style="margin-top:1rem;">Calculus prompts</div>', unsafe_allow_html=True)

prompt_cols = st.columns(2)
for idx, prompt in enumerate(PROMPTS):
    with prompt_cols[idx % 2]:
        if st.button(prompt, key=f"prompt_{idx}", use_container_width=True):
            st.session_state.pending_prompt = compose_prompt(prompt, st.session_state.mode)
            st.session_state.apply_nonce += 1
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
