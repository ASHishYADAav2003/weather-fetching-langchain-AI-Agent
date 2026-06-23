import os
import requests

from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate

from langchain_openai import ChatOpenAI

from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent
)

from ddgs import DDGS


# =====================================================
# LOAD ENV VARIABLES
# =====================================================

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")



# =====================================================
# NVIDIA LLM
# =====================================================

llm = ChatOpenAI(
    model="openai/gpt-oss-120b",
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY,
    temperature=0.5,
)


# =====================================================
# WEATHER TOOL
# =====================================================

@tool
def get_weather(city: str) -> str:
    """
    Get current weather information for a city.
    Use this tool whenever user asks about weather.
    """

    try:
        url = (
            f"http://api.weatherapi.com/v1/current.json"
            f"?key={WEATHER_API_KEY}&q={city}"
        )

        response = requests.get(url)
        data = response.json()

        if "error" in data:
            return data["error"]["message"]

        return f"""
City: {data['location']['name']}
Country: {data['location']['country']}
Temperature: {data['current']['temp_c']} °C
Condition: {data['current']['condition']['text']}
Humidity: {data['current']['humidity']}%
Wind Speed: {data['current']['wind_kph']} km/h
"""

    except Exception as e:
        return f"Weather Tool Error: {str(e)}"


# =====================================================
# DUCKDUCKGO SEARCH TOOL
# =====================================================



@tool
def web_search(query: str) -> str:
    """
    Search the internet using DuckDuckGo.
    Use this tool for:
    - Current events
    - Latest news
    - General facts
    - People
    - Companies
    - Technology questions
    """

    try:
        return duckduckgo.invoke(query)

    except Exception as e:
        return f"Search Tool Error: {str(e)}"


# =====================================================
# TOOLS
# =====================================================

tools = [
    get_weather,
    web_search
]


# =====================================================
# PROMPT
# =====================================================

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful AI assistant.

Available Tools:

1. get_weather
   - Use for weather related questions.

2. web_search
   - Use for internet searches.
   - Use for latest information.
   - Use for news.
   - Use for factual questions.

Always use tools whenever necessary.

Give concise and helpful answers.
"""
        ),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ]
)


# =====================================================
# CREATE AGENT
# =====================================================

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)


# =====================================================
# AGENT EXECUTOR
# =====================================================

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)


# =======================run agent==============================
response = agent_executor.invoke(
    {
        "input": "which caste is dominating in  etah ?"
    }
)

print("\nFinal Answer:\n")
print(response["output"])