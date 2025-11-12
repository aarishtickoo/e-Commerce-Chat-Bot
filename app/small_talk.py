from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

small_talk_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def small_talk(query):
    prompt = f"""
    You are an e-commerce chatbot designed to assist users with product-related queries and FAQs. 
    However, sometimes users may start with casual or small talk like greetings or introductory questions.

    If the user says something like:
    - "Hi", "Hello", "Hey", 
    - "How are you?", 
    - "What is your name?", 
    - "Who are you?", 
    - "What do you do?", 
    - or any other small talk or greeting message,

    then respond politely and naturally with a friendly tone using the following style:

    "Hi there! I’m an e-commerce chatbot here to help you with FAQs or any product-related queries. 
    Please type your question in the chat box to get started!"

    Keep the tone friendly, concise, and professional. 
    Do not provide unrelated or personal answers — always redirect the user gently toward using the chatbot for e-commerce assistance.
    """

    chat_completion = small_talk_client.chat.completions.create(
        model=os.environ["GROQ_MODEL"],
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": query}
        ]
    )

    response = chat_completion.choices[0].message
    return response.get("content") if isinstance(response, dict) else getattr(response, "content", str(response))


if __name__ == "__main__":
    # print (small_talk("Hi"))
    print (small_talk("What can I use you for?"))