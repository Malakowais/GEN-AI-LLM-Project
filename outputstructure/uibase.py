import streamlit as st
from dotenv import load_dotenv, parser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import Optional, List
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

from langchain.chat_models import init_chat_model

model = init_chat_model(
    "gemini-3.5-flash-lite",
    model_provider="google_genai"
)


class movie_info(BaseModel):
    movie_name: Optional[str]
    genre: Optional[str]
    director: Optional[str]
    release_year: Optional[str]
    main_cast: Optional[List[str]]
    main_character: Optional[List[str]]
    setting: Optional[str]
    plot: Optional[str]
    main_themes: Optional[List[str]]
    key_topics: Optional[List[str]]
    target_audience: Optional[str]
    overall_tone: Optional[str]
    quick_summary: Optional[str]
    one_line_summary: Optional[str]


parser = PydanticOutputParser(pydantic_object=movie_info)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        Extract useful and important information from the movie description provided below.
        {format_instructions}
        """
    ),
    (
        "human",
        """
        Extract useful and important information from the movie description provided below.
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

    /* animated gradient background */
    .stApp {
        background: linear-gradient(-45deg, #021b2b, #0b3a53, #12304f, #1b1464);
        background-size: 400% 400%;
        animation: bgmove 18s ease infinite;
        color: #eef6fb;
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
        filter: drop-shadow(0 0 20px rgba(45, 212, 191, .85));
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
        background: linear-gradient(90deg, #2dd4bf, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero p { color: #bcd3e0; font-weight: 300; margin-top: .3rem; }

    /* section label */
    .label {
        font-weight: 600;
        font-size: 1rem;
        color: #c9f5ee;
        margin: 1rem 0 .4rem 0;
    }

    /* text area */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
        border: 1px solid rgba(45, 212, 191, .5) !important;
        border-radius: 18px !important;
        padding: 1rem !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 28px rgba(0, 0, 0, .3);
    }
    .stTextArea textarea:focus {
        border-color: #2dd4bf !important;
        box-shadow: 0 0 0 3px rgba(45, 212, 191, .3) !important;
    }
    .stTextArea textarea::placeholder { color: #9bb7c7 !important; }
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
        background: linear-gradient(90deg, #0d9488, #3b82f6);
        box-shadow: 0 6px 22px rgba(13, 148, 136, .5);
        transition: all .25s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 10px 30px rgba(59, 130, 246, .55);
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
    [data-testid="stCode"] pre, [data-testid="stCode"] code {
        background: transparent !important;
        font-size: .9rem;
    }
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
        <p>Paste a movie description and get structured details instantly</p>
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
            {"paragraph": para,
             "format_instructions": parser.get_format_instructions()
             }
        )
        response = model.invoke(final_prompt)

    content = response.content
    if isinstance(content, list):
        content = "".join(
            part["text"] if isinstance(part, dict) else str(part)
            for part in content
        )

    # display only: remove ```json fences if the model added them
    content = content.strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[-1]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

    st.markdown('<div class="label">📋 Extracted Information</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.code(content, language="json")