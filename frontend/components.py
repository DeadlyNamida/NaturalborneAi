import streamlit as st


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(59,130,246,0.14), transparent 28%),
                radial-gradient(circle at bottom right, rgba(14,165,233,0.10), transparent 22%),
                linear-gradient(180deg, #030712 0%, #0b1220 45%, #0b1120 100%);
            color: #f8fafc;
        }

        .block-container {
            max-width: 1280px;
            padding-top: 4.2rem;
            padding-bottom: 2.2rem;
            padding-left: 1.8rem;
            padding-right: 1.8rem;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(15,23,42,0.98), rgba(17,24,39,0.98));
            border-right: 1px solid rgba(148,163,184,0.10);
        }

        [data-testid="stSidebar"] .block-container {
            padding-top: 1.8rem;
        }

        .hero {
            background: linear-gradient(135deg, rgba(15,23,42,0.92), rgba(17,24,39,0.88));
            border: 1px solid rgba(148,163,184,0.12);
            border-radius: 28px;
            padding: 2rem 2rem 1.7rem 2rem;
            box-shadow: 0 18px 60px rgba(0,0,0,0.32);
        }

        .hero-title {
            font-size: 3.1rem;
            line-height: 1;
            font-weight: 800;
            letter-spacing: -0.04em;
            margin: 0 0 0.8rem 0;
            color: #f8fafc;
        }

        .hero-sub {
            color: #cbd5e1;
            font-size: 1.03rem;
            line-height: 1.8;
            max-width: 820px;
            margin-bottom: 1rem;
        }

        .chip {
            display: inline-block;
            padding: 0.52rem 0.82rem;
            border-radius: 999px;
            background: rgba(37,99,235,0.14);
            border: 1px solid rgba(96,165,250,0.24);
            color: #dbeafe;
            font-size: 0.88rem;
            margin: 0.18rem 0.35rem 0.18rem 0;
        }

        .glass {
            background: rgba(15,23,42,0.72);
            border: 1px solid rgba(148,163,184,0.12);
            border-radius: 24px;
            padding: 1.15rem 1.1rem;
            box-shadow: 0 14px 38px rgba(0,0,0,0.18);
            height: 100%;
        }

        .label {
            color: #93c5fd;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.78rem;
            font-weight: 700;
            margin-bottom: 0.55rem;
        }

        .muted {
            color: #dbe3ef;
            font-size: 0.98rem;
            line-height: 1.7;
        }

        div[data-testid="stButton"] > button {
            width: 100%;
            border-radius: 999px;
            padding: 0.84rem 1.08rem;
            border: 1px solid rgba(96,165,250,0.24);
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: white;
            font-weight: 700;
            box-shadow: 0 10px 24px rgba(37,99,235,0.22);
        }

        div[data-testid="stButton"] > button:hover {
            border-color: rgba(147,197,253,0.45);
        }

        div[data-testid="stDownloadButton"] > button {
            width: 100%;
            border-radius: 16px;
        }

        @media (max-width: 900px) {
            .block-container {
                padding-top: 3.2rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
            .hero-title {
                font-size: 2.3rem;
            }
            .hero {
                padding: 1.35rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-title">{title}</div>
            <div class="hero-sub">{subtitle}</div>
            <div>
                <span class="chip">AnythingLLM</span>
                <span class="chip">Advanced chat</span>
                <span class="chip">Mode switching</span>
                <span class="chip">Modern UI</span>
                <span class="chip">Naturalborne workspace</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_info_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="glass">
            <div class="label">{title}</div>
            <div class="muted">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
