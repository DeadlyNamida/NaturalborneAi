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

PROMPT_LIBRARY = {
    "Limits": [
        "Solve this limit: lim(x→0) (sin x)/x.",
        "Evaluate lim(x→∞) (3x^2 + 1)/(x^2 - 4).",
        "Explain one-sided limits with a simple example.",
        "Use algebraic simplification to solve lim(x→2) (x^2-4)/(x-2).",
    ],
    "Derivatives": [
        "Differentiate x^3 ln(x) step by step.",
        "Find the derivative of e^(x^2) and explain each step.",
        "Use implicit differentiation on x^2 + y^2 = 25.",
        "Differentiate (x^2 + 1)/(x - 3) carefully.",
    ],
    "Integrals": [
        "Integrate sin(x)^2 from 0 to pi.",
        "Teach me u-substitution like a tutor.",
        "Integrate x e^(x^2) step by step.",
        "Use integration by parts on x cos(x).",
    ],
    "Applications": [
        "Find critical points and classify them for f(x)=x^3-3x^2+2.",
        "Solve an optimization problem involving area and perimeter.",
        "Explain concavity and points of inflection simply.",
        "Find where the function is increasing and decreasing.",
    ],
}

MODES = {
    "Step by step": "Work step by step. Show each step clearly and do not skip reasoning.",
    "Exam assistance": "Answer in exam style. Be concise, structured, and show working clearly.",
    "Concept tutoring": "Teach like a tutor. Explain the concept simply before solving.",
    "Error checking": "Check my work carefully. Point out mistakes and correct them clearly.",
}

THEMES = {
    "Ocean Blue": {
        "glow": "rgba(37,99,235,0.20)",
        "ring": "rgba(96,165,250,0.22)",
        "chip1": "rgba(37,99,235,0.94)",
        "chip2": "rgba(29,78,216,0.90)",
        "hero1": "rgba(15,23,42,0.94)",
        "hero2": "rgba(17,24,39,0.90)",
        "bg_radial_1": "rgba(59,130,246,0.14)",
        "bg_radial_2": "rgba(14,165,233,0.10)",
        "accent": "#93c5fd",
    },
    "Neon Violet": {
        "glow": "rgba(147,51,234,0.22)",
        "ring": "rgba(196,181,253,0.24)",
        "chip1": "rgba(147,51,234,0.94)",
        "chip2": "rgba(109,40,217,0.90)",
        "hero1": "rgba(20,18,35,0.94)",
        "hero2": "rgba(31,22,58,0.90)",
        "bg_radial_1": "rgba(168,85,247,0.14)",
        "bg_radial_2": "rgba(99,102,241,0.10)",
        "accent": "#c4b5fd",
    },
    "Emerald Night": {
        "glow": "rgba(16,185,129,0.22)",
        "ring": "rgba(110,231,183,0.22)",
        "chip1": "rgba(5,150,105,0.94)",
        "chip2": "rgba(4,120,87,0.90)",
        "hero1": "rgba(10,25,23,0.94)",
        "hero2": "rgba(14,37,33,0.90)",
        "bg_radial_1": "rgba(16,185,129,0.14)",
        "bg_radial_2": "rgba(45,212,191,0.10)",
        "accent": "#6ee7b7",
    },
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


def compose_prompt(base_prompt: str, mode_name: str, extra_instructions: str = "") -> str:
    parts = [MODES.get(mode_name, "").strip()]
    if extra_instructions.strip():
        parts.append(extra_instructions.strip())
    parts.append(base_prompt.strip())
    return "\n\n".join(part for part in parts if part)


def flatten_prompts() -> list[str]:
    prompts: list[str] = []
    for items in PROMPT_LIBRARY.values():
        prompts.extend(items)
    return prompts


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
      color: rgba(203, 213, 225, 0.74);
      font-size: 14px;
      padding: 2px 0 6px 2px;
      letter-spacing: 0.01em;
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
if "theme_name" not in st.session_state:
    st.session_state.theme_name = "Ocean Blue"
if "topic" not in st.session_state:
    st.session_state.topic = "Derivatives"
if "extra_instructions" not in st.session_state:
    st.session_state.extra_instructions = ""
if "prompt_clicks" not in st.session_state:
    st.session_state.prompt_clicks = 0

theme = THEMES[st.session_state.theme_name]
logo_b64 = image_to_base64("logo.png")

with st.sidebar:
    st.markdown("## Naturalborne")
    st.caption("Advanced Calculus Workspace")

    st.session_state.theme_name = st.selectbox(
        "Theme",
        list(THEMES.keys()),
        index=list(THEMES.keys()).index(st.session_state.theme_name),
    )

    st.session_state.mode = st.selectbox(
        "Default working mode",
        list(MODES.keys()),
        index=list(MODES.keys()).index(st.session_state.mode),
    )

    st.session_state.topic = st.selectbox(
        "Prompt topic",
        list(PROMPT_LIBRARY.keys()),
        index=list(PROMPT_LIBRARY.keys()).index(st.session_state.topic),
    )

    compact_header = st.toggle("Compact header", value=False)
    show_tips = st.toggle("Show study tips", value=True)
    show_stats = st.toggle("Show quick stats", value=True)

    st.markdown("---")
    st.caption("Make sure AnythingLLM is running on port 3001.")
    st.link_button("Open AnythingLLM", ANYTHINGLLM_HOST, use_container_width=True)

theme = THEMES[st.session_state.theme_name]
glow = f"0 0 0 1px {theme['ring']}, 0 30px 90px {theme['glow']}"
initial_chat_height = 720
hero_padding = "1.2rem 1.25rem 1.05rem" if compact_header else "1.65rem 1.7rem 1.45rem"
hero_title_size = "2.25rem" if compact_header else "2.85rem"

st.markdown(
    f"""
<style>
    .stApp {{
        background:
            radial-gradient(circle at top left, {theme["bg_radial_1"]}, transparent 26%),
            radial-gradient(circle at bottom right, {theme["bg_radial_2"]}, transparent 20%),
            linear-gradient(180deg, #020617 0%, #0b1220 48%, #0b1120 100%);
        color: #f8fafc;
    }}

    .block-container {{
        max-width: 1400px;
        padding-top: 1.8rem;
        padding-bottom: 1.35rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
    }}

    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(15,23,42,0.98), rgba(17,24,39,0.98));
        border-right: 1px solid rgba(148,163,184,0.10);
    }}

    [data-testid="stSidebar"] .block-container {{
        padding-top: 1.2rem;
    }}

    .nb-hero {{
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, {theme["hero1"]}, {theme["hero2"]});
        border: 1px solid rgba(148,163,184,0.12);
        border-radius: 32px;
        padding: {hero_padding};
        margin-bottom: 0.9rem;
        box-shadow: {glow};
        backdrop-filter: blur(16px);
    }}

    .nb-hero::before {{
        content: "";
        position: absolute;
        inset: -20% auto auto -10%;
        width: 320px;
        height: 320px;
        background: radial-gradient(circle, {theme["glow"]}, transparent 72%);
        pointer-events: none;
    }}

    .nb-brand {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
        position: relative;
        z-index: 2;
    }}

    .nb-brand-left {{
        display: flex;
        align-items: center;
        gap: 18px;
    }}

    .nb-logo-wrap {{
        width: 82px;
        height: 82px;
        border-radius: 26px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(15,23,42,0.74);
        border: 1px solid {theme["ring"]};
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
        font-size: {hero_title_size};
        line-height: 1;
        font-weight: 900;
        letter-spacing: -0.05em;
        color: #f8fafc;
    }}

    .nb-sub {{
        margin-top: 0.45rem;
        color: #d8e1ee;
        max-width: 860px;
        line-height: 1.68;
        font-size: 1rem;
    }}

    .nb-pill-row {{
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 0.95rem;
    }}

    .nb-pill {{
        padding: 0.62rem 0.92rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(148,163,184,0.12);
        color: #e6edf8;
        font-size: 0.88rem;
        font-weight: 600;
        backdrop-filter: blur(10px);
    }}

    .nb-kpi {{
        min-width: 140px;
        text-align: right;
    }}

    .nb-kpi-value {{
        font-size: 1.45rem;
        font-weight: 900;
        color: #fff;
        line-height: 1;
    }}

    .nb-kpi-label {{
        margin-top: 0.35rem;
        color: #bfd0ea;
        font-size: 0.85rem;
    }}

    .nb-glass {{
        background: rgba(15,23,42,0.72);
        border: 1px solid rgba(148,163,184,0.12);
        border-radius: 24px;
        padding: 1rem 1.1rem;
        box-shadow: 0 14px 38px rgba(0,0,0,0.16);
        backdrop-filter: blur(14px);
    }}

    .nb-card-title {{
        color: {theme["accent"]};
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 0.78rem;
        font-weight: 800;
        margin-bottom: 0.45rem;
    }}

    .nb-card-text {{
        color: #dbe3ef;
        font-size: 0.97rem;
        line-height: 1.66;
    }}

    .nb-embed {{
        margin-top: 10px;
        border-radius: 24px;
        overflow: visible;
        background: transparent;
    }}

    .nb-section {{
        margin-top: 16px;
    }}

    .nb-section-title {{
        color: #f8fafc;
        font-size: 1.08rem;
        font-weight: 900;
        margin: 0 0 0.8rem 0;
        letter-spacing: -0.02em;
    }}

    .nb-mode-note {{
        color: #a9bbd3;
        font-size: 0.94rem;
        margin-top: 0.42rem;
        line-height: 1.65;
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
        padding: 0.66rem 0.98rem;
    }}

    textarea {{
        border-radius: 18px !important;
    }}

    .stButton > button {{
        width: 100%;
        border-radius: 999px;
        border: 1px solid {theme["ring"]};
        background: linear-gradient(135deg, {theme["chip1"]}, {theme["chip2"]});
        color: white;
        font-weight: 800;
        padding: 0.82rem 1rem;
        box-shadow: 0 10px 28px rgba(0,0,0,0.15);
    }}

    .stButton > button:hover {{
        filter: brightness(1.04);
        transform: translateY(-1px);
    }}

    .nb-small {{
        color: #a9bbd3;
        font-size: 0.92rem;
        line-height: 1.65;
    }}

    .nb-footer-note {{
        margin-top: 10px;
        color: #8ea4c4;
        font-size: 0.88rem;
    }}

    @media (max-width: 950px) {{
        .block-container {{
            padding-top: 1.2rem;
            padding-left: 0.85rem;
            padding-right: 0.85rem;
        }}

        .nb-brand {{
            align-items: flex-start;
            flex-direction: column;
        }}

        .nb-brand-left {{
            align-items: flex-start;
        }}

        .nb-title {{
            font-size: 2.18rem;
        }}
    }}
</style>
""",
    unsafe_allow_html=True,
)

logo_html = f'<img src="data:image/png;base64,{logo_b64}" alt="Naturalborne logo">' if logo_b64 else ""
total_prompts = len(flatten_prompts())

st.markdown(
    f"""
<div class="nb-hero">
    <div class="nb-brand">
        <div class="nb-brand-left">
            <div class="nb-logo-wrap">{logo_html}</div>
            <div>
                <h1 class="nb-title">Naturalborne</h1>
                <div class="nb-sub">
                    A premium calculus workspace for guided problem solving, concept tutoring,
                    exam-style responses, and sharper mathematical writing in one polished interface.
                </div>
                <div class="nb-pill-row">
                    <div class="nb-pill">Current mode: {st.session_state.mode}</div>
                    <div class="nb-pill">Topic: {st.session_state.topic}</div>
                    <div class="nb-pill">Theme: {st.session_state.theme_name}</div>
                </div>
            </div>
        </div>
        <div class="nb-kpi">
            <div class="nb-kpi-value">{total_prompts}</div>
            <div class="nb-kpi-label">prompt starters</div>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

info_left, info_right = st.columns([1.45, 1])

with info_left:
    st.markdown(
        """
        <div class="nb-glass">
            <div class="nb-card-title">Workspace</div>
            <div class="nb-card-text">
                Use the embedded assistant for live calculus help, then refine your question with modes,
                topic prompts, and a custom builder underneath for cleaner, more advanced responses.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with info_right:
    st.markdown(
        """
        <div class="nb-glass">
            <div class="nb-card-title">Advanced features</div>
            <div class="nb-card-text">
                Auto-resizing embed, prompt injection, mode presets, themed interface,
                topic filtering, custom instructions, and reusable prompt composition.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

if show_stats:
    stats_cols = st.columns(4)
    stats_data = [
        ("Working mode", st.session_state.mode),
        ("Topic focus", st.session_state.topic),
        ("Prompt clicks", str(st.session_state.prompt_clicks)),
        ("Theme", st.session_state.theme_name),
    ]
    for col, (label, value) in zip(stats_cols, stats_data):
        with col:
            st.markdown(
                f"""
                <div class="nb-glass" style="padding:0.9rem 1rem;">
                    <div class="nb-card-title">{label}</div>
                    <div class="nb-card-text" style="font-weight:800;">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

if show_tips:
    st.markdown(
        """
        <div class="nb-glass" style="margin-top:14px; margin-bottom:12px;">
            <div class="nb-card-title">Study tips</div>
            <div class="nb-card-text">
                Pick a mode first, inject a prompt, then tweak the wording in the chat box.
                For better marks, ask for definitions, method choice, clean working, and a final boxed answer.
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

controls_left, controls_right = st.columns([1.15, 1])

with controls_left:
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

with controls_right:
    st.markdown('<div class="nb-section-title">Custom instruction booster</div>', unsafe_allow_html=True)
    st.session_state.extra_instructions = st.text_area(
        "Extra instructions",
        value=st.session_state.extra_instructions,
        height=112,
        placeholder="Example: Keep the explanation short, use exam notation, and include a final answer line.",
        label_visibility="collapsed",
    )
    st.markdown(
        '<div class="nb-small">These extra instructions get added before any clicked prompt.</div>',
        unsafe_allow_html=True,
    )

st.markdown('<div class="nb-section">', unsafe_allow_html=True)
st.markdown('<div class="nb-section-title">Prompt library</div>', unsafe_allow_html=True)

topic_tabs = st.tabs(list(PROMPT_LIBRARY.keys()))
for topic_name, tab in zip(PROMPT_LIBRARY.keys(), topic_tabs):
    with tab:
        prompt_cols = st.columns(2)
        for idx, prompt in enumerate(PROMPT_LIBRARY[topic_name]):
            with prompt_cols[idx % 2]:
                if st.button(prompt, key=f"{topic_name}_{idx}", use_container_width=True):
                    st.session_state.pending_prompt = compose_prompt(
                        prompt,
                        st.session_state.mode,
                        st.session_state.extra_instructions,
                    )
                    st.session_state.apply_nonce += 1
                    st.session_state.prompt_clicks += 1
                    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="nb-section">', unsafe_allow_html=True)
st.markdown('<div class="nb-section-title">Custom prompt builder</div>', unsafe_allow_html=True)

builder_col1, builder_col2 = st.columns([1.2, 1])
with builder_col1:
    custom_question = st.text_area(
        "Custom question",
        placeholder="Type your own calculus question here...",
        height=120,
        key="custom_question",
    )
with builder_col2:
    st.markdown(
        """
        <div class="nb-glass" style="height:100%;">
            <div class="nb-card-title">Prompt formula</div>
            <div class="nb-card-text">
                Mode preset + your extra instruction + question body.<br><br>
                This makes your requests look more deliberate, structured, and academically polished.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

builder_actions = st.columns([1, 1, 1])
with builder_actions[0]:
    if st.button("Inject custom prompt", use_container_width=True):
        if custom_question.strip():
            st.session_state.pending_prompt = compose_prompt(
                custom_question,
                st.session_state.mode,
                st.session_state.extra_instructions,
            )
            st.session_state.apply_nonce += 1
            st.session_state.prompt_clicks += 1
            st.rerun()
with builder_actions[1]:
    if st.button("Inject mode only", use_container_width=True):
        st.session_state.pending_prompt = compose_prompt(
            "Help me with a calculus problem.",
            st.session_state.mode,
            st.session_state.extra_instructions,
        )
        st.session_state.apply_nonce += 1
        st.session_state.prompt_clicks += 1
        st.rerun()
with builder_actions[2]:
    if st.button("Clear pending prompt", use_container_width=True):
        st.session_state.pending_prompt = ""
        st.session_state.apply_nonce += 1
        st.rerun()

st.markdown(
    """
    <div class="nb-footer-note">
        Tip: for a stronger presentation grade, demo multiple modes on the same problem and show how the interface adapts.
    </div>
    """,
    unsafe_allow_html=True,
)
