from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from core.summarizer_gemini import summarize
from core.triage_decision import triage
from core.llm_answerer import llm_answer
from core.rag_search import VectorDatabase
from core.web_search import answer_via_web

import google.generativeai as genai

load_dotenv()

router = APIRouter()

class EmailReq(BaseModel):
    email_text: str

@router.post("/process_email")
async def process_email(request: EmailReq):
    """
    Processes an email, extracts questions, and answers them using:
    1. RAG (retrieval from internal documents)
    2. LLM (general knowledge)
    3. WebSearch (live web search)
    """
    
    email_text = request.email_text

    # STEP 1: Extract questions from the email
    try:
        questions = summarize.summarize_to_points(email_text)
        if not questions:
            raise HTTPException(status_code=400, detail="No questions could be extracted.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error summarizing email: {str(e)}")

    # STEP 2: Prepare vector DB for RAG
    vector_db = VectorDatabase()
    answers = []

    # STEP 3: Process each question
    for question in questions:
        print(f"Processing question: {question}")

        # --- Try RAG first ---
        search_results = vector_db.similarity_search(question, threshold=0.5)

        if search_results:
            docs, sims = search_results
            # Merge relevant docs
            context = " ".join([d for d, s in zip(docs, sims) if s > 0.5])
            if context:
                prompt = f"Answer this question based on the context: {context}\n\nQuestion: {question}"
                model = genai.GenerativeModel(os.getenv("GEMINI_MODEL"))
                answer_text = model.generate_content(prompt).text.strip()
                answers.append({
                    "point": question,
                    "path": "RAG",
                    "answer": answer_text,
                    "justification": "Answer generated from internal documents"
                })
                continue  # Skip fallback if RAG worked

        # --- Fallback to triage ---
        triage_result = triage(question)
        print(f"Triage decision: {triage_result}")

        if triage_result["decision"] == "LLM":
            answer_text = llm_answer(question)
            answers.append({
                "point": question,
                "path": "LLM",
                "answer": answer_text,
                "justification": "Answer generated from LLM"
            })
        elif triage_result["decision"] == "WebSearch":
            answer_text = answer_via_web(question)
            if not answer_text:
                answer_text = "The current information could not be retrieved from the web search."
            answers.append({
                "point": question,
                "path": "WebSearch",
                "answer": answer_text,
                "justification": "Answer generated from live web search"
            })
        else:
            answers.append({
                "point": question,
                "path": "None",
                "answer": "No reliable answer found.",
                "justification": "Could not answer via RAG, LLM, or WebSearch"
            })

    return {
        "summary_points": questions,
        "answers": answers
    }
