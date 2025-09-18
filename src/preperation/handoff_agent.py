from agents import Agent , Runner , set_tracing_disabled , OpenAIChatCompletionsModel , RunConfig , enable_verbose_stdout_logging
from agents import ModelSettings , handoff , MaxTurnsExceeded
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
agent_C = Agent(
    name= "Agent C",
    instructions="You will answer of user query.",
    handoff_description="You are Agent C, you will answer of user query.",
    model=Model
)

agent_B = Agent(
    name="Agent B",
    instructions="You are Agent B you Must call to Agent C,",
    handoff_description="You are Agent B you Must Call to Agent C.",
    handoffs=[agent_C],
    model=Model

)

agent_A = Agent(
    name="Agent A",
    instructions="You are Agent A, you must call to agent B",
    handoffs=[agent_B],
    model=Model
)


async def main ():
   try:
        result = await Runner.run(
        agent_A,
        input="solve this math problem 12*15 and who is the president of Pakistan?",
        max_turns=3,
        )

        print("Final Output:")
        print(result.final_output)

   except MaxTurnsExceeded as e :
       print(e) 

def start ():
    asyncio.run(main())

