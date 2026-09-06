from langchain.tools import tool
#from langchain_community.utilities import TavilySearchAPIWrapper
from src.config import Config
from src.logger import logger
from langchain_community.tools import DuckDuckGoSearchRun

# Initialize DuckDuckGo Search (no API key required)
search_tool = DuckDuckGoSearchRun()

#tavily_search = TavilySearchAPIWrapper(tavily_api_key=Config.TAVILY_API_KEY)

@tool
def search_web_gaming_data(query: str) -> str:
    """Performs a web search using DuckDuckGo without API keys."""
    try:
        return search_tool.invoke(query)
    except Exception as e:
        return f"Web search error: {str(e)}"
        
'''
def search_web_gaming_data(query: str) -> str:
    """Searches the internet for real-time video game news, current developments, and missing game info."""
    logger.info(f"Tool Executing: search_web_gaming_data with query: '{query}'")
    try:
        results = tavily_search.results(query, max_results=3)
        formatted = [f"Source: {r['url']}\nContent: {r['content']}" for r in results]
        return "\n\n---\n\n".join(formatted)
    except Exception as e:
        logger.error(f"Web Search error: {str(e)}")
        return f"Web search failed due to error: {str(e)}"
'''
