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
("human",
 
        """
        Extract useful and important information from the movie description provided below.
        {paragraph}
        """
    )
]
)

para = input("Enter your paragraph: ")
final_prompt = prompt.invoke(
    {"paragraph": para,
    "format_instructions": parser.get_format_instructions()
     }
)
response = model.invoke(final_prompt)

print(response.content)