AI Email Summarizer & Intelligent Response Generator
AI Email Summarizer & Response Generator is a FastAPI-powered microservice designed to process incoming emails and generate actionable responses. The service uses **Google Gemini** to summarize email content into key questions, and then leverages **RAG (Vector DB)** for context-based answers or uses **LLM** (general knowledge) and **Web Search** for real-time information. The results are returned in a structured JSON format.

---

Features

- **Email Summarization**: Extracts key actionable questions or points from email text using **Google Gemini**.
- **Contextual Answer Generation**:
  - **RAG**: Searches a vector database for context and generates answers based on internal data.
  - **LLM**: Generates answers using general knowledge.
  - **Web Search**: Fetches real-time data from the web (using **Tavily** or other search APIs) when context isn't available.
- **Structured JSON Response**: Returns extracted questions, answers, and the response path in a clean JSON format.

---

## Tech Stack

- **Backend**: FastAPI
- **LLM**: Google Gemini API
- **Vector Database**: ChromaDB (for RAG layer)
- **Web Search**: Tavily API (for real-time information)
- **Environment Management**: dotenv for environment variables
- **Python**: Version 3.10+ 

---

## Setup

### Prerequisites

- Python 3.10 or higher
- Google Gemini API Key
- Tavily API Key
- ChromaDB (or other vector databases)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repo_url>
   cd <repo_directory>

  Set up your environment:

Create a virtual environment:

python3 -m venv venv


Activate the virtual environment:

On Windows:

.\venv\Scripts\activate


On macOS/Linux:

source venv/bin/activate
.env file
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
MAX_SNIPPETS=3


## Request Body:

{
  "email_text": "Hi team, before our Morocco tour launch, I wanted to ask: 1. What’s the best time to visit Chefchaouen? 2. How can we use Gemini with LangChain to generate itineraries? 3. Do we already have templates for desert tours?"
}

## Response
{
"summary_points": [
    "What’s the best time to visit Chefchaouen?",
    "How can we use Gemini with LangChain to generate itineraries?",
    "Do we have existing templates for desert tours?"
  ],
  "answers": [
    {
      "point": "What’s the best time to visit Chefchaouen?",
      "path": "Web Search",
      "answer": "The best time to visit Chefchaouen is between March and May or September and November when temperatures are mild.",
      "justification": "Factual travel timing question needing real-time info."
    },
    {
      "point": "How can we use Gemini with LangChain to generate itineraries?",
      "path": "LLM",
      "answer": "You can use Gemini as the reasoning engine within a LangChain agent, integrating retrieval tools to generate personalized itineraries.",
      "justification": "Conceptual system design question suitable for LLM reasoning."
    },
    {
      "point": "Do we have existing templates for desert tours?",
      "path": "RAG",
      "answer": "Yes, found internal document 'morocco_itineraries.txt' with prebuilt desert tour samples.",
      "justification": "Matching context found in vector database."
    }
  ]
}
