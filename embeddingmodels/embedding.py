from langchain_google_genai import GoogleGenerativeAIEmbeddings, embeddings
import os
from dotenv import load_dotenv
load_dotenv()
embeddings = GoogleGenerativeAIEmbeddings(
    model = "models/gemini-embedding-001",
    google_api_key = os.getenv("GOOGLE_API_KEY"),
    dimensions = 64
)

vector = embeddings.embed_query("What is Generative AI?")
print(vector)
