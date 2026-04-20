from __future__ import annotations

import json
from datetime import datetime
import streamlit as st

from services.anythingllm_client import AnythingLLMClient
from frontend.components import inject_styles, render_hero, render_info_card

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
    "Step-by-Step Mode": "Give the final answer first, then show full working and explanation step by step.",
    "Exam Mode": "Format the response as Task, Answer, and Working. Keep it neat and exam-ready.",
    "Concept Explanation": "Define the concept simply, then explain it clearly with an easy example if useful.",
    "Short Answer Mode": "Give only the final answer with very little explanation unless a step is necessary.",
    "Teaching Mode": "Explain slowly and clearly like a tutor helping a beginner understand each step.",
    "Error Checking": "Review the user's work carefully, point out mistakes, explain why they are wrong, and then show the corrected solution."
}

st.set_page_config(page_title="Naturalborne", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")
inject_styles()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = ""
if "base_url" not in st.session_state:
    st.session_state.base_url = "http://127.0.0.1:8001"
if "workspace_slug" not in st.session_state:
    st.session_state.workspace_slug = "naturalborne"
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "chat_path" not in st.session_state:
    st.session_state.chat_path = "/api/v1/workspace/{workspace_slug}/chat"
if "verify_ssl" not in st.session_state:
    st.session_state.verify_ssl = True
if "response_mode" not in st.session_state:
    st.session_state.response_mode = "Step-by-Step Mode"

def clear_chat():
    st.session_state.messages = []

def queue_prompt(text: str):
    st.session_state.pending_prompt = text

def export_chat() -> str:
    payload = {
        "created_at": datetime.utcnow().isoformat() + "Z",
        "base_url": st.session_state.base_url,
        "workspace_slug": st.session_state.workspace_slug,
        "response_mode": st.session_state.response_mode,
        "messages": st.session_state.messages,
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)

def build_client() -> AnythingLLMClient | None:
    if not st.session_state.base_url.strip() or not st.session_state.workspace_slug.strip() or not st.session_state.api_key.strip():
        return None
    return AnythingLLMClient(
        base_url=st.session_state.base_url,
        api_key=st.session_state.api_key,
        workspace_slug=st.session_state.workspace_slug,
        chat_path=st.session_state.chat_path,
        timeout_seconds=120,
        verify_ssl=st.session_state.verify_ssl,
    )

def extract_assistant_text(data: dict) -> str:
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

with st.sidebar:
    st.markdown("## Naturalborne")
    st.caption("AnythingLLM Workspace Frontend")

    st.text_input("Base URL", key="base_url", help="Example: http://127.0.0.1:8001")
    st.text_input("Workspace Slug", key="workspace_slug")
    st.text_input("AnythingLLM API Key", key="api_key", type="password")
    st.text_input("Chat Path", key="chat_path")
    st.checkbox("Verify SSL", key="verify_ssl")

    st.selectbox("Response Mode", list(MODE_GUIDANCE.keys()), key="response_mode")
    st.write(MODE_GUIDANCE[st.session_state.response_mode])

    client = build_client()
    if client is not None:
        ok, status = client.healthcheck()
        st.write(f"**Health:** {'OK' if ok else 'Issue'}")
        st.caption(status)
    else:
        st.write("**Health:** Not configured")

    if st.button("Clear Chat", use_container_width=True):
        clear_chat()
        st.rerun()

    st.download_button(
        "Download Chat JSON",
        data=export_chat(),
        file_name="naturalborne_chat.json",
        mime="application/json",
        use_container_width=True
    )

left, right = st.columns([1.7, 1])

with left:
    render_hero(
        "Naturalborne",
        "A Streamlit-native advanced chat page for your AnythingLLM workspace. "
        "Paste your base URL, workspace slug, and API key into the sidebar, then chat through a cleaner modern interface."
    )

with right:
    render_info_card(
        "How it connects",
        "The app sends each prompt to your configured AnythingLLM workspace chat endpoint and shows the returned response in the chat area below."
    )

st.subheader("Suggested prompts")
cols = st.columns(4)
for i, example in enumerate(SUGGESTED_PROMPTS):
    with cols[i % 4]:
        if st.button(example, use_container_width=True):
            queue_prompt(example)
            st.rerun()

st.divider()

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

    client = build_client()
    if client is None:
        answer = "Enter your Base URL, Workspace Slug, and AnythingLLM API Key in the sidebar first."
        with st.chat_message("assistant"):
            st.error(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    else:
        with st.chat_message("assistant"):
            try:
                raw = client.chat(message=prompt, mode=st.session_state.response_mode)
                answer = extract_assistant_text(raw)
                st.markdown(answer)
            except Exception as exc:
                answer = f"Request failed.\n\n`{exc}`"
                st.error(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})
