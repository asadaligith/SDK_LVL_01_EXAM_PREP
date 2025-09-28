from agents import OpenAIChatCompletionsModel 
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the OpenAI client
client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

Model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.5-flash",   
)
