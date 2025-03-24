import logging
from typing import List, Dict, Any

import requests
from bs4 import BeautifulSoup
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
            List of search results, each containing title, link, and snippet
        """
        try:
            logger.info(f"Running Baidu search for query: {query}")

            # Use the search_baidu method with the query and max_results
            results = self.search_baidu(query, num_results=self.max_results)

            if not results:
                logger.warning(f"No results found for query: {query}")
                return []

            return results

        except Exception as e:
            logger.error(f"Error during Baidu search: {str(e)}")
            return []

    def search_baidu(self, keyword, num_results=10, debug=0):
        """
        Search using keywords
        :param keyword: Search keyword
        :param num_results: Number of results to return
        :return: List of results
        """
        if not keyword:
            return None

        list_result = []
        page = 1

        baidu_search_url = "https://www.baidu.com/s?ie=utf-8&tn=baidu&wd="
        next_url = baidu_search_url + keyword

        while len(list_result) < num_results:
            data, next_url = self.parse_html(next_url, rank_start=len(list_result))
            if data:
                list_result += data
                if debug:
                    print(
                        "---searching[{}], finish parsing page {}, results number={}: ".format(
                            keyword, page, len(data)
                        )
                    )
                    for d in data:
                        print(str(d))

            if not next_url:
                if debug:
                    print("Already reached the last page.")
                break
            page += 1

        if debug:
            print(
                "\n---search [{}] finished. total results number={}!".format(
                    keyword, len(list_result)
                )
            )
        return (
            list_result[:num_results] if len(list_result) > num_results else list_result
        )

    def parse_html(self, url, rank_start=0, debug=0):
        """
        Parse and process search results
        :param url: URL to scrape
        :return: List of results and next page URL
        """
        HEADERS = {
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
            ),
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
            ),
            "Referer": "https://www.baidu.com/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        try:
            session = requests.Session()
            session.headers = HEADERS
            res = session.get(url=url)
            res.encoding = "utf-8"
            root = BeautifulSoup(res.text, "lxml")
            list_data = []
            div_contents = root.find("div", id="content_left")
            for div in div_contents.contents:
                if type(div) != type(div_contents):
                    continue

                class_list = div.get("class", [])
                if not class_list:
                    continue

                if "c-container" not in class_list:
                    continue

                title = ""
                url = ""
                abstract = ""
                try:
                    # Iterate through all found results to get title and summary content (within 50 characters)
                    if "xpath-log" in class_list:
                        if div.h3:
                            title = div.h3.text.strip()
                            url = div.h3.a["href"].strip()
                        else:
                            title = div.text.strip().split("\n", 1)[0]
                            if div.a:
                                url = div.a["href"].strip()

                        if div.find("div", class_="c-abstract"):
                            abstract = div.find("div", class_="c-abstract").text.strip()
                        elif div.div:
                            abstract = div.div.text.strip()
                        else:
                            abstract = div.text.strip().split("\n", 1)[1].strip()
                    elif "result-op" in class_list:
                        if div.h3:
                            title = div.h3.text.strip()
                            url = div.h3.a["href"].strip()
                        else:
                            title = div.text.strip().split("\n", 1)[0]
                            url = div.a["href"].strip()
                        if div.find("div", class_="c-abstract"):
                            abstract = div.find("div", class_="c-abstract").text.strip()
                        elif div.div:
                            abstract = div.div.text.strip()
                        else:
                            abstract = div.text.strip().split("\n", 1)[1].strip()
                    else:
                        if div.get("tpl", "") != "se_com_default":
                            if div.get("tpl", "") == "se_st_com_abstract":
                                if len(div.contents) >= 1:
                                    title = div.h3.text.strip()
                                    if div.find("div", class_="c-abstract"):
                                        abstract = div.find(
                                            "div", class_="c-abstract"
                                        ).text.strip()
                                    elif div.div:
                                        abstract = div.div.text.strip()
                                    else:
                                        abstract = div.text.strip()
                            else:
                                if len(div.contents) >= 2:
                                    if div.h3:
                                        title = div.h3.text.strip()
                                        url = div.h3.a["href"].strip()
                                    else:
                                        title = div.contents[0].text.strip()
                                        url = div.h3.a["href"].strip()
                                    if div.find("div", class_="c-abstract"):
                                        abstract = div.find(
                                            "div", class_="c-abstract"
                                        ).text.strip()
                                    elif div.div:
                                        abstract = div.div.text.strip()
                                    else:
                                        abstract = div.text.strip()
                        else:
                            if div.h3:
                                title = div.h3.text.strip()
                                url = div.h3.a["href"].strip()
                            else:
                                title = div.contents[0].text.strip()
                                url = div.h3.a["href"].strip()
                            if div.find("div", class_="c-abstract"):
                                abstract = div.find(
                                    "div", class_="c-abstract"
                                ).text.strip()
                            elif div.div:
                                abstract = div.div.text.strip()
                            else:
                                abstract = div.text.strip()
                except Exception as e:
                    if debug:
                        print(
                            "Caught exception during parsing page html, e={}".format(e)
                        )
                    continue
                ABSTRACT_MAX_LENGTH = 300  # abstract max length
                if ABSTRACT_MAX_LENGTH and len(abstract) > ABSTRACT_MAX_LENGTH:
                    abstract = abstract[:ABSTRACT_MAX_LENGTH]

                rank_start += 1
                list_data.append({"title": title, "content": abstract, "link": url})

            # Find the next page button
            next_btn = root.find_all("a", class_="n")

            # If this is the last page, return only the data without the next page link
            if len(next_btn) <= 0 or "Previous" in next_btn[-1].text:
                return list_data, None
            baidu_host_url = "https://www.baidu.com"
            next_url = baidu_host_url + next_btn[-1]["href"]
            return list_data, next_url
        except Exception as e:
            if debug:
                print("Caught exception during parsing page html, e: {}".format(e))
            return None, None

    async def _arun(self, query: str) -> List[Dict[str, Any]]:
        """
        Async version of the search tool.
        """
        # TODO: Implement async version if needed
        return self._run(query)


# test
if __name__ == "__main__":
    baidu_search = BaiduSearchTool(name="baidu_search", max_results=10)
    result = baidu_search.search_baidu("python")
    print(result)
