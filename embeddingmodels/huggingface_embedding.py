from langchain_huggingface import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
texts = ["What is Generative AI?",
         "hello how can I help you?",
          "Explain Generative AI in paragraph"
          ]
vector = embeddings.embed_documents(texts)
print(vector)