import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0.7
)

# ---------------------------------------------------------------- page setup
st.set_page_config(
    page_title="Generative AI Chatbot",
    page_icon="🤖",
    layout="centered",
)

# ---------------------------------------------------------------------- CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"], .stMarkdown, button, input, textarea {
        font-family: 'Poppins', sans-serif !important;
    }

    /* animated gradient background */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #1b1464, #302b63, #24243e);
        background-size: 400% 400%;
        animation: bgmove 18s ease infinite;
        color: #f1f1f8;
    }
    @keyframes bgmove {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* hide default chrome */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2rem; max-width: 820px; }

    /* hero */
    .hero {
        text-align: center;
        padding: 1.2rem 0 0.4rem 0;
    }
    .hero .logo {
        font-size: 3.4rem;
        filter: drop-shadow(0 0 18px rgba(139, 92, 246, .8));
        animation: float 3.5s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50%      { transform: translateY(-8px); }
    }
    .hero h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: .2rem 0 0 0;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero p {
        color: #b9b9d6;
        font-weight: 300;
        margin-top: .2rem;
    }

    /* mode cards */
    .mode-card {
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 22px;
        padding: 1.8rem 1.2rem 1.2rem 1.2rem;
        text-align: center;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        box-shadow: 0 10px 35px rgba(0, 0, 0, .35);
        transition: all .3s ease;
        min-height: 210px;
    }
    .mode-card:hover {
        transform: translateY(-6px);
        border-color: rgba(167, 139, 250, .8);
        box-shadow: 0 14px 40px rgba(139, 92, 246, .45);
    }
    .mode-card .emoji { font-size: 3rem; }
    .mode-card h3 {
        margin: .6rem 0 .3rem 0;
        font-weight: 600;
        color: white;
    }
    .mode-card p {
        color: #b9b9d6;
        font-size: .9rem;
        margin: 0;
    }

    /* buttons */
    .stButton > button {
        width: 100%;
        border: none;
        border-radius: 14px;
        padding: .7rem 1rem;
        font-weight: 600;
        color: white;
        background: linear-gradient(90deg, #7c3aed, #3b82f6);
        box-shadow: 0 6px 20px rgba(124, 58, 237, .45);
        transition: all .25s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 10px 28px rgba(59, 130, 246, .6);
        color: white;
    }

    /* mode badge */
    .badge-wrap { text-align: center; margin: .3rem 0 1.2rem 0; }
    .badge {
        display: inline-block;
        padding: .35rem 1rem;
        border-radius: 999px;
        font-size: .85rem;
        font-weight: 500;
        color: #e9e5ff;
        background: rgba(139, 92, 246, .22);
        border: 1px solid rgba(167, 139, 250, .55);
    }

    /* chat bubbles */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        padding: 1rem 1.2rem;
        margin-bottom: .9rem;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 6px 22px rgba(0, 0, 0, .25);
        animation: pop .35s ease;
    }
    @keyframes pop {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    [data-testid="stChatMessage"] p { color: #f4f4ff; line-height: 1.6; }

    /* chat input */
    [data-testid="stChatInput"] {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(167, 139, 250, .5);
        border-radius: 18px;
    }
    [data-testid="stChatInput"] textarea {
    color: black !important;
    background-color: white !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #666666 !important;
}

    /* expander */
    [data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
    }
    [data-testid="stExpander"] summary { color: #d8d4ff; font-weight: 500; }

    /* history rows */
    .hist-row {
        padding: .55rem .9rem;
        margin: .35rem 0;
        border-radius: 12px;
        font-size: .88rem;
        color: #ececff;
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #8b5cf6;
    }
    .hist-row.human  { border-left-color: #60a5fa; }
    .hist-row.ai     { border-left-color: #34d399; }
    .hist-row.system { border-left-color: #fbbf24; }
    .hist-role {
        font-weight: 600;
        font-size: .75rem;
        letter-spacing: .08em;
        text-transform: uppercase;
        opacity: .75;
        display: block;
        margin-bottom: .15rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------- hero
st.markdown(
    """
    <div class="hero">
        <div class="logo">🤖</div>
        <h1>Generative AI Chatbot</h1>
        <p>Pick a personality and start chatting</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------- mode selection
if "messages" not in st.session_state:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            """
            <div class="mode-card">
                <div class="emoji">😂</div>
                <h3>Funny AI Agent</h3>
                <p>Replies packed with jokes, puns and good vibes.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)
        if st.button("Choose Funny", key="funny"):
            st.session_state.messages = [
                SystemMessage(content="You are a funny AI Agent.")
            ]
            st.session_state.mode_label = "😂 Funny AI Agent"
            st.rerun()

    with col2:
        st.markdown(
            """
            <div class="mode-card">
                <div class="emoji">💡</div>
                <h3>Helpful AI Assistant</h3>
                <p>Clear, useful and to-the-point answers.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)
        if st.button("Choose Helpful", key="helpful"):
            st.session_state.messages = [
                SystemMessage(content="You are a helpful AI Assistant.")
            ]
            st.session_state.mode_label = "💡 Helpful AI Assistant"
            st.rerun()

    st.stop()

# ------------------------------------------------------------------ chat
messages = st.session_state.messages
mode_label = st.session_state.get("mode_label", "😂 Funny AI Agent")
bot_avatar = mode_label.split(" ")[0]

st.markdown(
    f"""
    <div class="badge-wrap">
        <span class="badge">Mode: {mode_label} &nbsp;•&nbsp; Type 'exit' to quit</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Render the chat so far (skip the system message)
for msg in messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="🧑"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar=bot_avatar):
            st.write(msg.content)

prompt = st.chat_input("Type your message here...")

if prompt:
    messages.append(HumanMessage(content=prompt))
    with st.chat_message("user", avatar="🧑"):
        st.write(prompt)

    if prompt.lower() == "exit":
        with st.chat_message("assistant", avatar=bot_avatar):
            st.write("Goodbye! 👋")
        st.stop()

    with st.spinner("Thinking..."):
        response = model.invoke(messages)

    messages.append(AIMessage(content=response.content))

    with st.chat_message("assistant", avatar=bot_avatar):
        st.write(response.content[0]["text"])

# ------------------------------------------------ conversation history
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("📜 Conversation History"):
    for msg in messages:
        if isinstance(msg, SystemMessage):
            role, css = "System", "system"
        elif isinstance(msg, HumanMessage):
            role, css = "Human", "human"
        else:
            role, css = "AI", "ai"

        content = msg.content
        if isinstance(content, list) and content and isinstance(content[0], dict):
            content = content[0].get("text", "")

        st.markdown(
            f'<div class="hist-row {css}"><span class="hist-role">{role}</span>{content}</div>',
            unsafe_allow_html=True,
        )