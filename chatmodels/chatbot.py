from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0.7
)
print("choose your ai mode")
print("1. Funny AI Agent")
print("2. Helpful AI Assistant")

choice = input("Enter your choice (1 or 2): ")

if choice == "1":
    system_message = SystemMessage(content="You are a funny AI Agent.")
elif choice == "2":
    system_message = SystemMessage(content="You are a helpful AI Assistant.")
else:
    print("Invalid choice. Defaulting to Funny AI Agent.")
    system_message = SystemMessage(content="You are a funny AI Agent.")

messages = [
    system_message
]

print("----- Welcome to the Generative AI Chatbot -----")
print("Type 'exit' to quit")

while True:
    prompt = input("You: ")
    messages.append(HumanMessage(content=prompt))
    if prompt.lower() == "exit":
        print("Chatbot: Goodbye! 👋")
        break


    response = model.invoke(messages)

    messages.append(AIMessage(content=response.content))

    print("Chatbot:", response.content[0]["text"])

    print("\n----- Conversation History -----",messages)

