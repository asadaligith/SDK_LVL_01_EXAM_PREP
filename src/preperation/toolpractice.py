from preperation.projectenv import Model , client 
from agents import Agent, Runner, set_tracing_disabled , function_tool , enable_verbose_stdout_logging, ModelSettings
import asyncio

enable_verbose_stdout_logging()
set_tracing_disabled(True)


@function_tool(is_enabled=True)
def get_weather(city: str) -> str:
    """returns weather info for the specified city."""
    return f"The weather in {city} is sunny"

agent = Agent(
    name="helput assistant",
    instructions="You are a Helpful assistant give the answer to user query",
    model=Model,
    tools=[get_weather],
    # model_settings=ModelSettings(tool_choice="none",)
    tool_use_behavior="stop_on_first_tool"
    
    
)
async def main():
    response = await Runner.run(starting_agent=agent, input="What is the weather in Karachi call tool", max_turns=1)

    print(response.final_output)

def start():
    asyncio.run(main())
