# tools/serp_search_tool.py

from ..config import SERP_API_KEY
import requests


class SerpSearchTool:
    def __init__(self):
        self.api_key = SERP_API_KEY

    def search_store(self, query):
        """Search for stores based on a query."""
        params = {
            "engine": "google",
            "q": query,
            "api_key": self.api_key
        }

        # Use the correct SERP API endpoint
        try:
            response = requests.get("https://serpapi.com", params=params)
            response.raise_for_status()
            results = response.json().get("organic_results", [])

            print(f'Serp API results: {results}')
            return [{"title": r["title"], "link": r["link"], "image": r.get("thumbnail")} for r in results]
        except requests.exceptions.RequestException as e:
            print(f"Error during SERP API search: {e}")
            return []
