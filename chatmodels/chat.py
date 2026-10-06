from dotenv import load_dotenv
import os

load_dotenv()
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "gemini-3.5-flash-lite",
    model_provider="google_genai"
)

response = model.invoke(
    "Explain Generative ai in paragraph"
)

print(response.content)