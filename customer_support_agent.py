from gemini_llm import query_gemini

def get_support_response(user_question):
    system_prompt = """
    You are a helpful and experienced customer support agent for an insurance company.
    Answer questions briefly, clearly, and accurately. Use real-world examples where helpful.
    """
    final_prompt = f"{system_prompt}\n\nUser: {user_question}\n\nAgent:"
    response = query_gemini(final_prompt)
    return response.strip()