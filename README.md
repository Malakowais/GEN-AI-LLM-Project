# Generative AI Project

This project is a practical learning and experimentation repository for Generative AI using Python, LangChain, and multiple LLM providers. It includes examples for chat-based interactions, embeddings, prompt-driven extraction, and output-structured responses.

## Overview

The project demonstrates how to:

- Connect to LLM providers such as Google Gemini, OpenAI, and xAI
- Use LangChain for model initialization and prompt handling
- Generate embeddings for semantic search and vector tasks
- Build simple chatbot interfaces
- Extract structured data from unstructured text using Pydantic models
- Explore UI-based demo variations of core AI workflows

## Tech Stack

- Python
- LangChain
- LangChain Core
- LangChain Community
- LangChain Google Generative AI
- LangChain Hugging Face
- OpenAI SDK
- Google GenAI SDK
- xAI SDK
- Python dotenv
- Pydantic

## Project Structure

```text
GENERATIVE AI/
├── .env                         # Environment variables for API keys
├── requirements.txt            # Project dependencies
├── test.py                     # Basic environment/version check
├── chatmodels/                 # Chatbot-related examples
│   ├── chat.py                 # Interactive Gemini chatbot with mode selection
│   ├── chatbot.py              # Simple LangChain chat model demo
│   ├── huggingface.py          # Hugging Face model example
│   └── uichatbot.py            # UI-based chatbot variant
├── embeddingmodels/            # Embedding generation examples
│   ├── embedding.py            # Google Gemini embeddings example
│   └── huggingface_embedding.py # Hugging Face embedding example
├── outputstructure/            # Structured output parsing examples
│   ├── base.py                 # Pydantic structured extraction example
│   └── uibase.py               # UI variant of structured output handling
├── cincage/                    # Additional demo scripts
│   ├── core.py                 # Core generative AI workflow example
│   └── uicore.py               # UI-oriented variant
├── .venv/                      # Local virtual environment
├── venv/                       # Secondary local environment
└── README.md                   # Project documentation
```

## Setup

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate the environment:

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Configure API keys in a `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
XAI_API_KEY=your_xai_api_key
HUGGINGFACEHUB_API_TOKEN=your_hf_token
```

## Usage

Run the scripts individually depending on the feature you want to test.

### Chatbot example

```bash
python chatmodels/chat.py
```

### Simple LangChain chatbot demo

```bash
python chatmodels/chatbot.py
```

### Google embeddings example

```bash
python embeddingmodels/embedding.py
```

### Hugging Face embedding example

```bash
python embeddingmodels/huggingface_embedding.py
```

### Structured extraction example

```bash
python outputstructure/base.py
```

## Notes

- Some scripts are interactive and expect user input from the terminal.
- Several examples rely on external API keys and internet connectivity.
- The repository is best suited for learning, experimentation, and prototyping rather than production deployment.
- You may need to adjust model names and provider configuration depending on your account access and available model versions.

## Example Features Covered

- AI chat conversations
- Multi-provider LLM access
- Embedding generation
- Vector representation examples
- Prompt templating
- Structured JSON-like outputs using Pydantic
- Basic GenAI experimentation workflows

## License

This project is intended for educational and personal experimentation. Add a license if you plan to share or distribute it publicly.

## Next Ideas

- Add Streamlit or Flask UI for a better user experience
- Add a proper project package structure
- Add unit tests for prompt and parser logic
- Add documentation for model provider configuration
- Create reusable helper modules for API setup and environment checks
