import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()

from langchain.chat_models import init_chat_model

model = init_chat_model(
    "gemini-3.5-flash-lite",
    model_provider="google_genai"
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert information extraction assistant.

Extract useful and important information from the movie description provided below.

Return the information in the following structure:

Movie Information:
- Movie Name:
- Genre:
- Director:
- Release Year:
- Main Cast:
- Main Character(s):
- Setting:
- Plot:
- Main Themes:
- Key Topics:
- Target Audience:
- Overall Tone:
- Quick Summary:
- One-Line Summary:

Important instructions:
1. Extract only information that is explicitly mentioned or can be safely inferred from the given text.
2. Do not invent missing information.
3. If a field is not available, write "Not mentioned".
4. Keep the extracted information clear and concise.
5. The Quick Summary should be 2-3 sentences.
6. The One-Line Summary should be a single sentence.
7. Separate facts clearly from the summary.
8. Focus on useful information rather than repeating the original paragraph.
"""
    ),
    (
        "human",
        """
Extract useful and important information from the movie description provided below.

Return the information in the following structure:

{paragraph}
"""
    )
])

# ---------------------------------------------------------------- page setup
st.set_page_config(
    page_title="Movie Information Extractor",
    page_icon="🎬",
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

    /* animated cinematic gradient background */
    .stApp {
        background: linear-gradient(-45deg, #1a0b2e, #3d0a4f, #7a1f3d, #1b1464);
        background-size: 400% 400%;
        animation: bgmove 18s ease infinite;
        color: #f4f1fb;
    }
    @keyframes bgmove {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* hide default chrome */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2rem; max-width: 860px; }

    /* hero */
    .hero { text-align: center; padding: 1.2rem 0 1rem 0; }
    .hero .logo {
        font-size: 3.6rem;
        filter: drop-shadow(0 0 20px rgba(251, 113, 133, .85));
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
        background: linear-gradient(90deg, #fb7185, #f59e0b, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero p { color: #cfc6e6; font-weight: 300; margin-top: .3rem; }

    /* section label */
    .label {
        font-weight: 600;
        font-size: 1rem;
        color: #ffd9e0;
        margin: 1rem 0 .4rem 0;
    }

    /* text area */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.08) !important;
        color: #000000 !important;
        border: 1px solid rgba(251, 113, 133, .5) !important;
        border-radius: 18px !important;
        padding: 1rem !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 28px rgba(0, 0, 0, .3);
    }
    .stTextArea textarea:focus {
        border-color: #fb7185 !important;
        box-shadow: 0 0 0 3px rgba(251, 113, 133, .3) !important;
    }
    .stTextArea textarea::placeholder { color: #b7abd4 !important; }
    .stTextArea label { display: none; }

    /* button */
    .stButton > button {
        width: 100%;
        border: none;
        border-radius: 14px;
        padding: .75rem 1rem;
        font-weight: 600;
        font-size: 1rem;
        color: white;
        background: linear-gradient(90deg, #e11d48, #f59e0b);
        box-shadow: 0 6px 22px rgba(225, 29, 72, .5);
        transition: all .25s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 10px 30px rgba(245, 158, 11, .55);
        color: white;
    }

    /* result card */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 22px !important;
        padding: .6rem 1.2rem;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        box-shadow: 0 10px 35px rgba(0, 0, 0, .35);
        animation: pop .4s ease;
    }
    @keyframes pop {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    [data-testid="stVerticalBlockBorderWrapper"] p,
    [data-testid="stVerticalBlockBorderWrapper"] li {
        color: #f6f2ff;
        line-height: 1.7;
    }
    [data-testid="stVerticalBlockBorderWrapper"] strong { color: #fcd34d; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------- hero
st.markdown(
    """
    <div class="hero">
        <div class="logo">🎬</div>
        <h1>Movie Information Extractor</h1>
        <p>Paste a movie description and get the key details instantly</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------------- input
st.markdown('<div class="label">🎞️ Enter your paragraph</div>', unsafe_allow_html=True)
para = st.text_area(
    "Enter your paragraph",
    height=220,
    placeholder="Paste or type the movie description here...",
)

extract = st.button("✨ Extract Information")

# ------------------------------------------------------------------- output
if extract:
    with st.spinner("Extracting information..."):
        final_prompt = prompt.invoke(
            {"paragraph": para}
        )
        response = model.invoke(final_prompt)

    content = response.content
    if isinstance(content, list):
        content = "".join(
            part["text"] if isinstance(part, dict) else str(part)
            for part in content
        )

    st.markdown('<div class="label">📋 Extracted Information</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(content)