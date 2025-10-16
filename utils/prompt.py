Summarize_prompt = """
Summarize the following email into a concise list of clear, standalone, answerable questions  that reflect the key points in the email such that even if there are any grammatical errors in the questions,correct it without destroying the semantic meaning of the overall question.
Return only a JSON array of strings.
Email:
{placeholder_for_email}

"""

RAG_ANSWER_PROMPT = """You are a precise assistant. Use ONLY the provided context to answer. 
If the context is insufficient, say "I don't have enough info."
Context:
{context}

Question: {question}

Answer clearly and concisely in about one short paragraph with no styling just plain text. Remove any unnecessary symbols:
"""

TRIAGE_PROMPT = """For the question below, decide whether the answer should be retrieved from **LLM** (general knowledge) or **WebSearch** (real-time facts, events, or specific real-world data).
- If the question is about **current facts, people, places, events, or real-world data** (e.g., "Who is the president of the USA?"), use **WebSearch**.
- If the question is **conceptual**, **technical**, or related to a **how-to** (e.g., "How to set up a database?" or "Explain machine learning"), use **LLM**.
Return JSON: {"decision": "LLM" | "WebSearch", "reason": "<short reason>"}.
Question: {question}

"""

LLM_ANSWER_PROMPT = """Answer clearly and concisely in about one short paragraph with no styling just plain text
Question: {question}
Answer clearly and concisely in about one short paragraph with no styling just plain text"""

WEB_SYNTH_PROMPT = """Synthesize a **short and accurate and latest** answer using the web snippets below. Do not cite any sources—just provide the latest and current answer based on the information given.
Snippets:
{snippets}

Question: {question}

Answer clearly and concisely in about one short paragraph with no styling just plain text
"""
