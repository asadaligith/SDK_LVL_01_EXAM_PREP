from agents import Agent , Runner , set_tracing_disabled , OpenAIChatCompletionsModel , RunConfig , enable_verbose_stdout_logging
from openai import AsyncOpenAI
from dotenv import load_dotenv
import asyncio
import os

enable_verbose_stdout_logging()
# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
set_tracing_disabled(True)

# Initialize the OpenAI client
client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

Model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.5-flash",   
)


simple_agent = Agent(
    name="Simple Agent",
    instructions="You are a helpful assistant that responds to user queries.",
)


async def main ():
    result = await Runner.run(
        simple_agent,
        input="What's the capital of France?",
        run_config=RunConfig(model=Model )
    )

    print(f"Result Type",type(result))

    print("Final Output:")
    print(result.final_output)

def start ():
    asyncio.run(main())

