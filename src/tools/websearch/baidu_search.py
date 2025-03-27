import logging
from typing import List, Dict, Any
from baidusearch.baidusearch import search
from langchain.tools import BaseTool

logger = logging.getLogger(__name__)
BAIDU_MAX_RESULTS = 10


class BaiduSearchTool(BaseTool):
    name: str = "baidu_search"
    description: str = (
        "Search the internet using Baidu search engine. Input should be a search query."
    )
    max_results: int = BAIDU_MAX_RESULTS

    def __init__(
        self,
        name,
        max_results: int = BAIDU_MAX_RESULTS,
    ):
        super().__init__()
        self.name = name
        self.max_results = max_results

    def _run(self, query: str) -> List[Dict[str, Any]]:
        """
        Run Baidu search with the given query.

        Args:
            query: The search query string

        Returns:
            List of search results, each containing title, link, and content
        """
        try:
            logger.info(f"Running Baidu search for query: {query}")
            # Use the search_baidu method with the query and max_results
            results = search(query, num_results=self.max_results)
            if not results:
                logger.warning(f"No results found for query: {query}")
                return []
            format_results = [
                {
                    "title": result["title"],
                    "content": result["abstract"],
                    "link": result["url"],
                }
                for result in results
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


# test
if __name__ == "__main__":
    baidu_search = BaiduSearchTool(name="baidu_search", max_results=10)
    result = baidu_search._run("python")
    print(result)
