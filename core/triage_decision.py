from pydantic import BaseModel
import google.generativeai as genai
import os

# Define the triage decision function
def triage(question: str) -> dict:
    """
    Decides whether the answer should be retrieved from LLM (for conceptual/technical questions)
    or from WebSearch (for factual/real-time data questions).
    
    Args:
        question (str): The question to classify.
    
    Returns:
        dict: Decision and reasoning for the path to take.
    """
    # Define the triage prompt (fixed the format specifier issue)
    triage_prompt = f"""
    For the question below, decide whether the answer should be retrieved from **LLM** (general knowledge) or **WebSearch** (real-time facts, events, or specific real-world data).
    - If the question is about **current facts, people, places, events, or real-world data** (e.g., "Who is the president of the USA?"), use **WebSearch**.
    - If the question is **conceptual**, **technical**, or related to a **how-to** (e.g., "How to set up a database?" or "Explain machine learning"), use **LLM**.
    Return JSON in the following format:
    {{
        "decision": "LLM" or "WebSearch",
        "reason": "<short reason>"
    }}
    Question: {question}
    """

    # Use Gemini to generate the decision
    model = genai.GenerativeModel(os.getenv("GEMINI_MODEL"))
    decision_response = model.generate_content(triage_prompt)

    # Parse the response
    decision = decision_response.text.strip().lower()

    if "websearch" in decision:
        return {"decision": "WebSearch", "reason": "Real-time data or factual information required"}
    elif "llm" in decision:
        return {"decision": "LLM", "reason": "Conceptual or technical knowledge required"}
    else:
        return {"decision": "LLM", "reason": "Fallback to LLM as no clear decision could be made"}
