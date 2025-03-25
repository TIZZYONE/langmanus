import logging
from typing import List, Dict, Any
from langchain.tools import BaseTool
from langchain_community.tools.bing_search import BingSearchResults

logger = logging.getLogger(__name__)
BING_MAX_RESULTS = 10


class BingSearchTool(BaseTool):
    name: str = "bing_search"
    description: str = (
        "Search the internet using Bing search engine. Input should be a search query."
    )
    max_results: int = BING_MAX_RESULTS

    def __init__(self, name, max_results: int = BING_MAX_RESULTS):
        super().__init__()
        self.name = name
        self.max_results = max_results
        self.bing_search = BingSearchResults()

    def _run(self, query: str) -> List[Dict[str, Any]]:
        """
        Run Bing search with the given query.

        Args:
            query: The search query string

        Returns:
            List of search results, each containing title, link, and snippet
        """
        try:
            logger.info(f"Running Bing search for query: {query}")
            results = self.bing_search.run(query)
            
            if not results:
                logger.warning(f"No results found for query: {query}")
                return []

            # Convert the results to the expected format
            formatted_results = []
            for result in results[:self.max_results]:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "content": result.get("snippet", "")
                })
            
            return formatted_results

        except Exception as e:
            logger.error(f"Error during Bing search: {str(e)}")
            return []

    async def _arun(self, query: str) -> List[Dict[str, Any]]:
        """
        Async version of the search tool.
        """
        # TODO: Implement async version if needed
        return self._run(query)


# test
if __name__ == "__main__":
    bing_search = BingSearchTool(name="bing_search", max_results=10)
    result = bing_search._run("python")
    print(result)
