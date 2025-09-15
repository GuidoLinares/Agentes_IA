import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from tools import weather_tool
from tools import end_conversation_tool

load_dotenv()

memory = MemorySaver()

tavily_tool = TavilySearch(max_results = 2)

### TOOLS PARA EL CHAT ###
tools = [tavily_tool,weather_tool,end_conversation_tool]

llm = ChatGoogleGenerativeAI(model ="gemini-2.5-flash",
                            google_api_key = os.getenv("GOOGLE_API_KEY"))
llm_with_tools = llm.bind_tools(tools)


graph_config = {"configurable": {"thread_id":"1"}}









