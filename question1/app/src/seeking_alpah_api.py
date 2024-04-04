import requests
from typing import Dict, List


class SeekingAlphaAPI:

    def __init__(self, api_key: str, api_host: str):
        """
        Seeking alpha api handler class.

        Args:
            api_key: Seeking Alpha API key.
            api_host: Seeking Alpha API Host url.
        """
        self.headers = {"X-RapidAPI-Key": api_key,
                        "X-RapidAPI-Host": api_host}

    def get_company_info(self, company_symbol: str) -> Dict | None:
        """
        Requests more detailed company info such as the company name by company symbol.

        Args:
            company_symbol: Company symbol such as TSLA.

        Returns:
            Returns company info as Dict or None if company info was not found.
        """
        response = requests.get("https://seeking-alpha.p.rapidapi.com/symbols/get-profile", headers=self.headers,
                                params={"symbols": company_symbol}).json()
        if response["data"][0]["tickerId"] is None:
            return None
        else:
            return response

    def get_latest_news(self, company_symbol: str, number_of_articles: int = 3) -> List[Dict]:
        """
        Request a list of the latest news by company symbol from seeking alpha.

        Args:
            company_symbol: Company symbol such as TSLA.
            number_of_articles: Number of news articles that shall be requested.

        Returns:
            Returns List of articles in form of dictionaries.

        """
        return requests.get("https://seeking-alpha.p.rapidapi.com/news/v2/list-by-symbol",
                            headers=self.headers,
                            params={"id": company_symbol, "size": number_of_articles}).json()

    def get_article_by_id(self, id: str) -> Dict:
        """
        Request detailed information such as article content by article ID from seeking alpha.

        Args:
            id: Seeking Alpha article ID.

        Returns:
            Detailed article info as dict.
        """
        return requests.get("https://seeking-alpha.p.rapidapi.com/news/get-details",
                            headers=self.headers,
                            params={"id": id}).json()
