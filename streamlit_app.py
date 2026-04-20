import json
from datetime import datetime

import requests
import streamlit as st

# =========================================================
# EMBEDDED CONNECTION SETTINGS
# =========================================================
# Paste your actual values here before running.
ANYTHINGLLM_BASE_URL = "http://127.0.0.1:3001"
ANYTHINGLLM_API_KEY = "GPWSNPA-X2Q4VAC-PR1D626-3ZWMQQ6"
WORKSPACE_SLUG = "naturalborne"
CHAT_PATH = "/v1/workspace/natualborne/chat"
VERIFY_SSL = True
TIMEOUT_SECONDS = 120

SUGGESTED_PROMPTS = [
    "Differentiate $3x^2 + 5x - 7$ step by step.",
    "Explain the chain rule in simple terms.",
    "Evaluate $\\lim_{x \\to 2} \\frac{x^2 - 4}{x - 2}$.",
    "Solve this in exam mode: Differentiate $(2x-3)^5$.",
    "Check my working for this integral.",
    "Explain integration like I am a beginner.",
    "Give the final answer only for $\\frac{dy}{dx}(x^4)$.",
    "Teach me how to solve derivative word problems."
]

MODE_GUIDANCE = {
    "Step-by-Step Mode": "Full working with each step shown clearly.",
    "Exam Mode": "Neat answer format with task, answer, and working.",
    "Concept Explanation": "Simple explanation with a clear example if needed.",
    "Short Answer Mode": "Final answer first with very little extra detail.",
    "Teaching Mode": "Slower explanation like a tutor helping a student.",
    "Error Checking": "Review the work, find mistakes, and correct them."
}

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = ""

if "response_mode" not in st.session_state:
    st.session_state.response_mode = "Step-by-Step Mode"


def clear_chat() -> None:
    st.session_state.messages = []


def queue_prompt(text: str) -> None:
    st.session_state.pending_prompt = text


def export_chat() -> str:
    payload = {
        "created_at": datetime.utcnow().isoformat() + "Z",
        "mode": st.session_state.response_mode,
        "messages": st.session_state.messages,
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def build_url() -> str:
    return f"{ANYTHINGLLM_BASE_URL.rstrip('/')}{CHAT_PATH.format(workspace_slug=WORKSPACE_SLUG)}"


def healthcheck() -> tuple[bool, str]:
    try:
        response = requests.get(
            f"{ANYTHINGLLM_BASE_URL.rstrip('/')}/api/docs",
            timeout=min(TIMEOUT_SECONDS, 20),
            verify=VERIFY_SSL,
        )
        if response.ok:
            return True, "Ready"
        return False, f"Unavailable ({response.status_code})"
    except Exception as exc:
        return False, str(exc)


def extract_response_text(data: dict) -> str:
    for key in ("textResponse", "response", "message"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value

    if isinstance(data.get("messages"), list) and data["messages"]:
        last = data["messages"][-1]
        if isinstance(last, dict):
            for key in ("content", "text", "message"):
                value = last.get(key)
                if isinstance(value, str) and value.strip():
                    return value

    return json.dumps(data, indent=2, ensure_ascii=False)


def send_message(message: str, mode: str) -> str:
    response = requests.post(
        build_url(),
        headers={
            "Authorization": f"Bearer {ANYTHINGLLM_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        json={
            "message": message,
            "mode": mode,
        },
        timeout=TIMEOUT_SECONDS,
        verify=VERIFY_SSL,
    )
    response.raise_for_status()
    data = response.json()
    return extract_response_text(data)


st.set_page_config(
    page_title="Naturalborne",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(59,130,246,0.16), transparent 24%),
            radial-gradient(circle at bottom right, rgba(14,165,233,0.10), transparent 18%),
            linear-gradient(180deg, #030712 0%, #0b1220 42%, #101826 100%);
        color: #f8fafc;
    }

    .block-container {
        max-width: 1320px;
        padding-top: 4rem;
        padding-bottom: 2.2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15,23,42,0.99), rgba(17,24,39,0.99));
        border-right: 1px solid rgba(148,163,184,0.10);
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 1.8rem;
    }

    .nb-hero {
        background:
            linear-gradient(135deg, rgba(15,23,42,0.94), rgba(17,24,39,0.90));
        border: 1px solid rgba(148,163,184,0.10);
        border-radius: 32px;
        padding: 2.2rem 2.2rem 2rem 2.2rem;
        box-shadow: 0 22px 70px rgba(0,0,0,0.34);
    }

    .nb-logo-wrap {
        display: flex;
        justify-content: center;
        margin-bottom: 0.7rem;
    }

    .nb-title {
        text-align: center;
        font-size: 3.4rem;
        line-height: 1;
        font-weight: 800;
        letter-spacing: -0.05em;
        margin: 0 0 0.8rem 0;
    }

    .nb-sub {
        text-align: center;
        max-width: 860px;
        margin: 0 auto 1rem auto;
        color: #d7e0ee;
        line-height: 1.85;
        font-size: 1.06rem;
    }

    .nb-chip-row {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 0.4rem;
    }

    .nb-chip {
        display: inline-flex;
        padding: 0.55rem 0.86rem;
        border-radius: 999px;
        background: rgba(37,99,235,0.14);
        border: 1px solid rgba(96,165,250,0.22);
        color: #dbeafe;
        font-size: 0.88rem;
    }

    .nb-card {
        background: rgba(15,23,42,0.76);
        border: 1px solid rgba(148,163,184,0.12);
        border-radius: 24px;
        padding: 1.15rem 1.1rem;
        box-shadow: 0 12px 34px rgba(0,0,0,0.16);
        height: 100%;
    }

    .nb-label {
        color: #93c5fd;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 0.78rem;
        font-weight: 700;
        margin-bottom: 0.55rem;
    }

    .nb-text {
        color: #dbe3ef;
        font-size: 0.98rem;
        line-height: 1.72;
    }

    .nb-section-title {
        font-size: 1.95rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-top: 1.15rem;
        margin-bottom: 0.5rem;
    }

    .nb-section-sub {
        color: #b8c6d9;
        line-height: 1.7;
        margin-bottom: 0.85rem;
    }

    div[data-testid="stButton"] > button {
        width: 100%;
        border-radius: 999px;
        padding: 0.88rem 1.08rem;
        border: 1px solid rgba(96,165,250,0.22);
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: white;
        font-weight: 700;
        box-shadow: 0 10px 26px rgba(37,99,235,0.22);
    }

    div[data-testid="stButton"] > button:hover {
        border-color: rgba(147,197,253,0.45);
    }

    div[data-testid="stDownloadButton"] > button {
        width: 100%;
        border-radius: 16px;
    }

    hr {
        border-color: rgba(148,163,184,0.10) !important;
    }

    @media (max-width: 900px) {
        .block-container {
            padding-top: 3rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .nb-title {
            font-size: 2.5rem;
        }

        .nb-hero {
            padding: 1.45rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

ok, status = healthcheck() if ANYTHINGLLM_BASE_URL.strip() and ANYTHINGLLM_API_KEY.strip() else (False, "Not configured")

with st.sidebar:
    st.markdown("## Naturalborne")
    st.caption("Study Workspace")

    st.selectbox(
        "Study Mode",
        list(MODE_GUIDANCE.keys()),
        key="response_mode",
    )
    st.write(MODE_GUIDANCE[st.session_state.response_mode])

    st.markdown("---")
    st.write(f"**Workspace:** `{WORKSPACE_SLUG}`")
    st.write(f"**Status:** {'Ready' if ok else 'Unavailable'}")
    st.caption(status)

    if st.button("Clear Chat", use_container_width=True):
        clear_chat()
        st.rerun()

    st.download_button(
        "Download Chat JSON",
        data=export_chat(),
        file_name="naturalborne_chat.json",
        mime="application/json",
        use_container_width=True,
    )

hero_left, hero_right = st.columns([1.65, 1])

with hero_left:
    st.markdown('<div class="nb-hero">', unsafe_allow_html=True)
    st.markdown('<div class="nb-logo-wrap">', unsafe_allow_html=True)
    try:
        st.image("logo.png", width=110)
    except Exception:
        pass
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="nb-title">Naturalborne</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="nb-sub">A focused study space for calculus. Work through derivatives, integrals, limits, exam questions, and corrections with clearer structure and a stronger study flow.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="nb-chip-row">
            <span class="nb-chip">Step by step</span>
            <span class="nb-chip">Exam support</span>
            <span class="nb-chip">Concept help</span>
            <span class="nb-chip">Error review</span>
            <span class="nb-chip">Math-friendly formatting</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

with hero_right:
    st.markdown(
        f"""
        <div class="nb-card">
            <div class="nb-label">Current Mode</div>
            <div class="nb-text"><strong>{st.session_state.response_mode}</strong><br>{MODE_GUIDANCE[st.session_state.response_mode]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    ready_text = (
        "Everything is set for chat."
        if ok
        else "Add your connection values in the file before using the workspace."
    )
    st.markdown(
        f"""
        <div class="nb-card">
            <div class="nb-label">Session</div>
            <div class="nb-text">{ready_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="nb-section-title">Start with one of these</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="nb-section-sub">Pick a prompt below or type your own question into the chat box.</div>',
    unsafe_allow_html=True,
)

cols = st.columns(4)
for i, example in enumerate(SUGGESTED_PROMPTS):
    with cols[i % 4]:
        if st.button(example, use_container_width=True):
            queue_prompt(example)
            st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

pending_prompt = st.session_state.pending_prompt
prompt = st.chat_input("Ask a calculus question...")

if pending_prompt and not prompt:
    prompt = pending_prompt
    st.session_state.pending_prompt = ""

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not ANYTHINGLLM_BASE_URL.strip() or not ANYTHINGLLM_API_KEY.strip():
        answer = "Add your base URL and key in the file first."
        with st.chat_message("assistant"):
            st.error(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    else:
        with st.chat_message("assistant"):
            try:
                answer = send_message(prompt, st.session_state.response_mode)
                st.markdown(answer)
            except Exception as exc:
                answer = f"Request failed.\n\n`{exc}`"
                st.error(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
