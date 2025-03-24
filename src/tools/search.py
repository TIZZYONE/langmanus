import logging
from langchain_community.tools.tavily_search import TavilySearchResults
from src.config.tools import MAX_RESULTS
from .decorators import create_logged_tool
from .websearch import BaiduSearchTool,BingSearchTool

logger = logging.getLogger(__name__)

# Initialize Tavily search tool with logging
LoggedTavilySearch = create_logged_tool(TavilySearchResults)
search_tool = LoggedTavilySearch(name="tavily_search", max_results=MAX_RESULTS)

# Initialize Baidu search tool with logging
# LoggedBaiduSearch = create_logged_tool(BaiduSearchTool)
# search_tool = LoggedBaiduSearch(name="baidu_search", max_results=MAX_RESULTS)

# Initialize Bing search tool with logging
# LoggedBaiduSearch = create_logged_tool(BingSearchTool)
# search_tool = LoggedBaiduSearch(name="baidu_search", max_results=MAX_RESULTS)