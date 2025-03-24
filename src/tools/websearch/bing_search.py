import logging
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
from langchain.tools import BaseTool

logger = logging.getLogger(__name__)
BING_MAX_RESULTS = 10

class BingSearchTool(BaseTool):
    name: str = "bing_search"
    description: str = "Search the internet using Bing search engine. Input should be a search query."
    max_results: int = BING_MAX_RESULTS

    def __init__(self, name, max_results: int = BING_MAX_RESULTS):
        super().__init__()
        self.name = name
        self.max_results = max_results

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
            
            # Use the search_bing method with the query and max_results
            results = self.search_bing(query, num_results=self.max_results)
            
            if not results:
                logger.warning(f"No results found for query: {query}")
                return []
                
            return results
            
        except Exception as e:
            logger.error(f"Error during Bing search: {str(e)}")
            return []

    def search_bing(self, query: str, num_results: int = 10) -> List[Dict[str, str]]:
        """
        Search using keywords
        :param query: Search keyword
        :param num_results: Number of results to return
        :return: List of results
        """
        if not query:
            return []

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        }
        search_url = f"https://www.bing.com/search?q={query}"

        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            # Set the correct encoding before accessing response.text
            # The previous approach was incorrect - we need to set it to the detected encoding
            if response.encoding.lower() != 'utf-8':
                response.encoding = response.apparent_encoding
            html = response.text
            # Don't print the entire HTML which can be very large
            logger.debug(f"Received HTML response with encoding: {response.encoding}")
        except requests.RequestException as e:
            logger.error(f"Error fetching Bing search results: {e}")
            return []

        soup = BeautifulSoup(html, 'html.parser')
        results = []

        for result in soup.select('.b_algo')[:num_results]:
            a_tag = result.find('a', href=True)
            h2_tag = result.find('h2')
            p_tag = result.find('p')

            title = h2_tag.get_text() if h2_tag else ''
            link = a_tag['href'] if a_tag else ''
            snippet = p_tag.get_text() if p_tag else ''

            # Only log shorter versions for debugging
            logger.debug(f"Found result: {title[:30]}... - {link[:30]}...")

            if link and title:
                result_info = {
                    "title": title,
                    "link": link,
                    "content": snippet,
                }
                results.append(result_info)

        return results

    async def _arun(self, query: str) -> List[Dict[str, Any]]:
        """
        Async version of the search tool.
        """
        # TODO: Implement async version if needed
        return self._run(query)



#test
if __name__ == "__main__":
    baidu_search = BingSearchTool(name="bing_search", max_results=10)
    result = baidu_search.search_bing("python")
    print(result)