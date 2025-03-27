from langchain_community.tools.tavily_search import TavilySearchResults
from src.config.tools import MAX_RESULTS
from src.config import SEARCH_ENGINE
from .decorators import create_logged_tool
from .websearch import BaiduSearchTool,GoogleSearchTool

SEARCH_TOOLS = {
    "tavily": TavilySearchResults,
    "baidu": BaiduSearchTool,
    "google": GoogleSearchTool,
}

# Initialize search tool based on configuration
if SEARCH_ENGINE not in SEARCH_TOOLS:
    raise ValueError(f"Unsupported search engine: {SEARCH_ENGINE}")


ToolClass = SEARCH_TOOLS[SEARCH_ENGINE]
LoggedSearchTool = create_logged_tool(ToolClass)
search_tool = LoggedSearchTool(name=f"{SEARCH_ENGINE}_search", max_results=MAX_RESULTS)
