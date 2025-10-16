import os
from utils.prompt import LLM_ANSWER_PROMPT
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY", ""))
MODEL = os.getenv("GEMINI_MODEL")

def _model():
    return genai.GenerativeModel(MODEL)

def llm_answer(question: str) -> str:
    prompt = LLM_ANSWER_PROMPT.format(question=question)
    return _model().generate_content(prompt).text.strip()
