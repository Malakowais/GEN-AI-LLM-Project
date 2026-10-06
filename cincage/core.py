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

para = input("Enter your paragraph: ")
final_prompt = prompt.invoke(
    {"paragraph": para}
)
response = model.invoke(final_prompt)

print(response.content)