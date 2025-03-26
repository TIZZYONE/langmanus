from langchain_community.tools.tavily_search import TavilySearchResults
from src.config.tools import MAX_RESULTS
from src.config import SEARCH_ENGINE
from .decorators import create_logged_tool
from .websearch import BaiduSearchTool

# Initialize search tool based on configuration
LoggedTavilySearch = create_logged_tool(TavilySearchResults)
LoggedBaiduSearch = create_logged_tool(BaiduSearchTool)

if SEARCH_ENGINE == "tavily":
    search_tool = LoggedTavilySearch(name="tavily_search", max_results=MAX_RESULTS)
elif SEARCH_ENGINE == "baidu":
    search_tool = LoggedBaiduSearch(name="baidu_search", max_results=MAX_RESULTS)
else:
    raise ValueError(f"Unsupported search engine: {SEARCH_ENGINE}")
