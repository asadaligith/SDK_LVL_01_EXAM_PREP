from preperation.projectenv import Model , client 
from agents import Agent, Runner, set_tracing_disabled , function_tool , enable_verbose_stdout_logging, ModelSettings
import asyncio
from agents import RunContextWrapper
from dataclasses import dataclass

enable_verbose_stdout_logging()
set_tracing_disabled(True)

@dataclass
class UserInformation:
    name: str
    uid : int
    
@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInformation]) -> str:  
    """Fetch the age of the user. Call this function to get user's age information."""
    return f"The user {wrapper.context.name} is 28 years old"

@function_tool(is_enabled=True)
def get_weather(city: str) -> str:
    """returns weather info for the specified city."""
    return f"The weather in {city} is sunny"

async def main():
    User_info = UserInformation(name="Asad Ali", uid=123,)

    agent = Agent[User_info](
        name="helput assistant",
        instructions="You are a Helpful assistant give the answer to user query",
        model=Model,
        tools=[get_weather , fetch_user_age],    
        
    )

    response = await Runner.run(starting_agent=agent, input="What is the age of User", context=User_info)

    print(response.final_output)

def start():
    asyncio.run(main())
