import os, json
from dotenv import load_dotenv
import google.generativeai as genai
from utils.prompt import Summarize_prompt

load_dotenv()

class EmailSummarizer:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel(os.getenv("GEMINI_MODEL"))

    def summarize_to_points(self, actual_text: str):
        # If input is very short, treat it as a single question
        # if len(actual_text.split()) < 15:  
        #     return [actual_text]

        prompt = Summarize_prompt.format(placeholder_for_email=actual_text)
        response = self.model.generate_content(prompt).text.strip()

        # Remove any Markdown code formatting
        if response.startswith("```"):
            response = "\n".join(response.splitlines()[1:-1])

        try:
            questions = json.loads(response)
            if isinstance(questions, list) and all(isinstance(q, str) for q in questions):
                return questions
        except json.JSONDecodeError:
            # fallback: treat raw output as single question
            return [actual_text]

        return [actual_text]

summarize = EmailSummarizer()
