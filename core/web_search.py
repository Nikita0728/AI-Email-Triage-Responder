import os
from tavily import TavilyClient
from utils.prompt import WEB_SYNTH_PROMPT
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
MAX_SNIPPETS = int(os.getenv("MAX_SNIPPETS", "3"))

# Initialize Tavily client
client = TavilyClient(api_key=TAVILY_API_KEY)



def answer_via_web(question: str) -> str:
    """
    Fetch latest web snippets for a question and synthesize an answer using Gemini.
    """
    try:
        # Step 1: Search web with 'fresh=True' to get latest results
        results = client.search(query=question, max_results=MAX_SNIPPETS, fresh=True)
        print("Raw Tavily search results:", results)  # Log raw response for debugging

        # Step 2: Safely get snippets list
        snippets_list = results.get("results") or results.get("result") or []
        if not snippets_list:
            print("No snippets found in the search results.")
            return "No web snippets found."

        # Step 3: Combine all snippets into one string
        snippets_list = results.get("results") or results.get("result") or []
        combined_snippets = " ".join(r.get("content", "") for r in snippets_list)


        if not combined_snippets:
            return "No web snippets available to generate answer."

        # Step 4: Prepare prompt for Gemini
        prompt = WEB_SYNTH_PROMPT.format(snippets=combined_snippets, question=question)
        print("Generated Prompt:", prompt)  # Log the final prompt

        # Step 5: Use Gemini model to generate the answer
        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(prompt)

        # Step 6: Safely extract text
        answer = ""
        if hasattr(response, "text") and response.text:
            answer = response.text.strip()
        else:
            answer = "Unable to generate an answer from web snippets."

        return answer

    except Exception as e:
        print(f"Error in answer_via_web function: {e}")
        return "Error processing the web search or generating answer."

