
from agents import Agent , Runner , OpenAIChatCompletionsModel , set_tracing_disabled , enable_verbose_stdout_logging
from openai import AsyncOpenAI
from agents import MaxTurnsExceeded , function_tool , AgentHooks , handoff , HandoffInputData
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


class MyAgentHooks(AgentHooks):
    async def on_start(self, context, agent):
        print(f"✅ {agent.name} is Start here")

    async def on_end(self, context, agent, output):
        print(f"❤️ {agent.name} Ends here: Output {output}")

    async def on_tool_start(self, context, agent, tool):
        print(f"💜 {tool} is Started ")
    
    async def on_tool_end(self, context, agent, tool, result):
        print(f"😊 {tool} is Ends result is : {result} ")

    async def on_handoff(self, context, agent, source):
        print(f"🗒️ {agent.name} take over control to the {source}")


def simple_filter(data : HandoffInputData )-> HandoffInputData :
     print("Handoff Input Filter")
     summerize = "Get Latest input data"
     return HandoffInputData(
         input_history=summerize,
         pre_handoff_items=(),
         new_items=()
     )


@function_tool
async def weather_tool(location:str)->str:
    """You fetch the weather of givin location"""
    return f"The Current weather of {location} is sunny"

joke_agent = Agent(name="Joke Agent", instructions="You Tell the Joke to the User",model=Model, )

assistant_agent = Agent(
    name="helpful assistant",
    instructions="you are a helpfull assistant you give answer of user query if user ask about jokes you must call to joke agent",
    tools=[weather_tool],
    handoffs=[handoff(joke_agent, input_filter=simple_filter)],
    model=Model,
    hooks=MyAgentHooks()

)

async def main ():
   try:
        result = await Runner.run(
        assistant_agent,
        input="What is the weather of Karachi & and also tell two funny jokes",
        max_turns=7,
        )

        print("Final Output:")
        print(result.final_output)

   except MaxTurnsExceeded as e :
       print(e) 

def start ():
    asyncio.run(main())

