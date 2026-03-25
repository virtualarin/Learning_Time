import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Mode Chat",
    page_icon="✦",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=DM+Mono:wght@300;400&display=swap');

/* ── Root & Reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f;
    color: #e8e6f0;
    font-family: 'DM Mono', monospace;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(99,60,200,.35) 0%, transparent 60%),
        #0a0a0f;
}

/* hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Typography ── */
h1, h2, h3 { font-family: 'Syne', sans-serif; }

/* ── App shell ── */
.block-container {
    max-width: 760px !important;
    padding: 2rem 1.5rem 6rem !important;
}

/* ── Header ── */
.app-header {
    text-align: center;
    padding: 2.5rem 0 2rem;
}
.app-header .logo {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #b794f4, #7c3aed, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.app-header .sub {
    margin-top: .4rem;
    font-size: .78rem;
    color: #6b6880;
    letter-spacing: .12em;
    text-transform: uppercase;
}

/* ── Mode pills ── */
.mode-badge {
    display: inline-flex;
    align-items: center;
    gap: .45rem;
    padding: .3rem .9rem;
    border-radius: 999px;
    font-family: 'Syne', sans-serif;
    font-size: .8rem;
    font-weight: 600;
    letter-spacing: .04em;
    margin: 0 auto 1.6rem;
    border: 1px solid rgba(255,255,255,.08);
}
.mode-comedy   { background: rgba(251,191,36,.12);  color: #fbbf24; border-color: rgba(251,191,36,.3); }
.mode-motivate { background: rgba(52,211,153,.12);  color: #34d399; border-color: rgba(52,211,153,.3); }
.mode-data     { background: rgba(56,189,248,.12);  color: #38bdf8; border-color: rgba(56,189,248,.3); }

/* ── Mode selector cards ── */
.stRadio > label { display: none; }          /* hide "Mode" label above radio */
div[data-testid="stHorizontalBlock"] { gap: 0; }

/* Streamlit radio buttons → pill style */
.stRadio div[role="radiogroup"] {
    display: flex;
    gap: .6rem;
    flex-wrap: wrap;
    justify-content: center;
    margin-bottom: 1.2rem;
}
.stRadio div[role="radiogroup"] label {
    cursor: pointer;
    padding: .55rem 1.2rem;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,.12);
    background: rgba(255,255,255,.04);
    font-family: 'Syne', sans-serif;
    font-size: .82rem;
    font-weight: 600;
    color: #a09bb8;
    transition: all .2s ease;
}
.stRadio div[role="radiogroup"] label:hover {
    background: rgba(124,58,237,.2);
    border-color: rgba(124,58,237,.5);
    color: #c4b5fd;
}
.stRadio div[role="radiogroup"] label[data-checked="true"],
.stRadio div[role="radiogroup"] [aria-checked="true"] ~ span {
    background: rgba(124,58,237,.3);
    border-color: #7c3aed;
    color: #ede9fe;
}
/* hide the actual radio circle */
.stRadio div[role="radiogroup"] input { display: none; }

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(124,58,237,.4), transparent);
    margin: 1.2rem 0;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: .15rem 0 !important;
}

/* User bubble */
[data-testid="stChatMessage"][data-testid*="user"],
.stChatMessage:has([data-testid="chatAvatarIcon-user"]) .stChatMessageContent {
    background: rgba(124,58,237,.18) !important;
    border: 1px solid rgba(124,58,237,.3) !important;
    border-radius: 18px 18px 4px 18px !important;
}

/* Assistant bubble */
.stChatMessage:has([data-testid="chatAvatarIcon-assistant"]) .stChatMessageContent {
    background: rgba(255,255,255,.04) !important;
    border: 1px solid rgba(255,255,255,.08) !important;
    border-radius: 18px 18px 18px 4px !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    border-radius: 14px !important;
    border: 1px solid rgba(124,58,237,.4) !important;
    background: rgba(255,255,255,.04) !important;
    font-family: 'DM Mono', monospace !important;
    color: #e8e6f0 !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,.2) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(124,58,237,.4); border-radius: 4px; }

/* ── Reset / New chat button ── */
.stButton button {
    background: rgba(255,255,255,.05) !important;
    border: 1px solid rgba(255,255,255,.1) !important;
    color: #a09bb8 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: .75rem !important;
    border-radius: 8px !important;
    padding: .35rem .9rem !important;
    transition: all .2s ease !important;
}
.stButton button:hover {
    border-color: rgba(124,58,237,.5) !important;
    color: #c4b5fd !important;
    background: rgba(124,58,237,.12) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="logo">✦ AI Mode Chat</div>
    <div class="sub">powered by Gemini 2.5 Flash Lite</div>
</div>
""", unsafe_allow_html=True)

# ── Mode selector ─────────────────────────────────────────────────────────────
MODE_CONFIG = {
    "😂  Comedy": {
        "system": "You are a comedian",
        "badge_class": "mode-comedy",
        "icon": "😂",
        "label": "Comedy Mode",
    },
    "🔥  Motivational": {
        "system": "You are a motivational speaker",
        "badge_class": "mode-motivate",
        "icon": "🔥",
        "label": "Motivational Mode",
    },
    "📊  Data Scientist": {
        "system": "You are a professional data scientist",
        "badge_class": "mode-data",
        "icon": "📊",
        "label": "Data Scientist Mode",
    },
}

selected_mode = st.radio(
    "Mode",
    options=list(MODE_CONFIG.keys()),
    horizontal=True,
    label_visibility="collapsed",
)

cfg = MODE_CONFIG[selected_mode]

# Active mode badge
st.markdown(
    f'<div style="text-align:center">'
    f'<span class="mode-badge {cfg["badge_class"]}">'
    f'{cfg["icon"]} {cfg["label"]}'
    f'</span></div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {k: [] for k in MODE_CONFIG}

if "last_mode" not in st.session_state:
    st.session_state.last_mode = selected_mode

# ── Reset button ─────────────────────────────────────────────────────────────
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("↺ Clear", use_container_width=False):
        st.session_state.chat_histories[selected_mode] = []
        st.rerun()

# ── Retrieve current history ──────────────────────────────────────────────────
history = st.session_state.chat_histories[selected_mode]

# ── Render chat history ───────────────────────────────────────────────────────
for msg in history:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input(f"Message {cfg['label']}…"):
    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    history.append(HumanMessage(content=prompt))

    # Build full message list with system prompt
    full_messages = [SystemMessage(content=cfg["system"])] + history

    # Call the model
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

    with st.chat_message("assistant"):
        with st.spinner(""):
            response = model.invoke(full_messages)
            st.markdown(response.content)

    history.append(AIMessage(content=response.content))
    st.session_state.chat_histories[selected_mode] = history