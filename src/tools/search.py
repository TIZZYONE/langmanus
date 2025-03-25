import logging
from langchain_community.tools.tavily_search import TavilySearchResults
from src.config.tools import MAX_RESULTS
from .decorators import create_logged_tool
from .websearch import BaiduSearchTool, BingSearchTool
from src.config.config import get_config

logger = logging.getLogger(__name__)
a = os.environ["SEARCH_TOOL"]

def get_search_tool():
    config = get_config()
    search_config = config.get('SEARCH_CONFIG', {})
    search_tool_name = search_config.get('search_tool', 'tavily')
    max_results = search_config.get('max_results', MAX_RESULTS)

    if search_tool_name == 'tavily':
        LoggedTavilySearch = create_logged_tool(TavilySearchResults)
        return LoggedTavilySearch(name="tavily_search", max_results=max_results)
    elif search_tool_name == 'baidu':
        LoggedBaiduSearch = create_logged_tool(BaiduSearchTool)
        return LoggedBaiduSearch(name="baidu_search", max_results=max_results)
    elif search_tool_name == 'bing':
        LoggedBingSearch = create_logged_tool(BingSearchTool)
        return LoggedBingSearch(name="bing_search", max_results=max_results)
    else:
        logger.warning(f"Unknown search tool: {search_tool_name}, falling back to Tavily")
        LoggedTavilySearch = create_logged_tool(TavilySearchResults)
        return LoggedTavilySearch(name="tavily_search", max_results=max_results)

search_tool = get_search_tool()
