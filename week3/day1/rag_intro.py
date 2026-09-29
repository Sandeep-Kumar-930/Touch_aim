
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"


# Step 1: Knowledge Base
knowledge_base = {
    "age": "The age of Pratyush is 25 years",
    "net worth": "The net worth of Pratyush is 2000"
}

# Step 2: Retrieval
def retrieve_info(question):
    question = question.lower()

    if "age" in question:
        return knowledge_base["age"]

    elif "net worth" in question:
        return knowledge_base["net worth"]

    else:
        return None

# Step 3: Ask LLM
def ask_llm(question):

    context = retrieve_info(question)

    print("\nRetrieved Context:", context)

    if context is None:
        return "Sorry, I don't have information about that in my knowledge base."

    sys_prompt = f"""
    Answer in one line only.
    Answer only based on this context.
    Do not hallucinate.

    Context: {context}
    """

    system_message = {
        "role": "system",
        "content": sys_prompt
    }

    message = {
        "role": "user",
        "content": question
    }

    messages = [system_message, message]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )

    answer = response.choices[0].message.content

    return answer

# Step 4: Ask Question
question = "What is Pratyush's age?"

print("\nFinal Answer:", ask_llm(question))