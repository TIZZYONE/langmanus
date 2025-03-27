import logging
from typing import List, Dict, Any
from baidusearch.baidusearch import search
from langchain.tools import BaseTool

from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import Tool
import os

logger = logging.getLogger(__name__)
GOOGLE_MAX_RESULTS = 10

# 环境变量中配置API密钥
os.environ["SERPER_API_KEY"] = "a043e5913a4edd809010ca6d2789cbb2882e76e9"


class GoogleSearchTool(BaseTool):
    name: str = "google_search"
    description: str = (
        "Search the internet using google search engine. Input should be a search query."
    )
    max_results: int = GOOGLE_MAX_RESULTS

    def __init__(
        self,
        name,
        max_results: int = GOOGLE_MAX_RESULTS,
    ):
        super().__init__()
        self.name = name
        self.max_results = max_results

    def _run(self, query: str) -> List[Dict[str, Any]]:
        """
        Run Goole search with the given query.

        Args:
            query: The search query string

        Returns:
            List of search results, each containing title, link, and content
        """
        try:
            logger.info(f"Running Google search for query: {query}")
            # Use the search_baidu method with the query and max_results
            results = GoogleSerperAPIWrapper().results(
                query=query, num_results=self.max_results
            )
            if not results:
                logger.warning(f"No results found for query: {query}")
                return []
            format_results = [
                {
                    "title": result["title"],
                    "content": result["snippet"],
                    "link": result["link"],
                }
                for result in results["organic"]
            ]

            return format_results

        except Exception as e:
            logger.error(f"Error during Baidu search: {str(e)}")
            return []

    async def _arun(self, query: str) -> List[Dict[str, Any]]:
        """
        Async version of the search tool.
        """
        # TODO: Implement async version if needed
        return self._run(query)


# # test
if __name__ == "__main__":
    google_search = GoogleSearchTool(name="google_search", max_results=10)
    result = google_search._run("python")
    print(result)


# from serpapi.google_search import GoogleSearch
#
# params = {
#   "engine": "google",
#   "q": "Coffee",
#   "api_key": "c0958e15270eb91fcff076f4b3184f8b0c7cf3665db2fda32a2f3b5964b4fa88"
# }
#
# search = GoogleSearch(params)
# results = search.get_dict()
# print(results)
# organic_results = results["organic_results"]
# print(organic_results)
