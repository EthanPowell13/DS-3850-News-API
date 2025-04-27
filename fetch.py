# fetch.py
import requests
from typing import List, Dict
from config import NEWS_API_KEY
from summarize import article_keyword
def fetch_articles(
    query: str,
    max_results: int = 10,
    language: str = "en"
) -> List[Dict]:
    """
    Fetches up to `max_results` recent articles matching `query`.
    Returns list of article dicts with keys:
      - title
      - description
      - url
      - publishedAt
      - content
    """
    endpoint = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "pageSize": max_results,
        "language": language,
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY,
    }

    response = requests.get(endpoint, params=params)
    response.raise_for_status()  # throws if the call failed
    payload = response.json()
    return payload.get("articles", [])

if __name__ == "__main__":
    # Quick manual test
    test_query = article_keyword
    print(f"Fetching top 5 articles for: {test_query!r}\n")
    content = []
    articles = fetch_articles(test_query, max_results=5)
    for idx, art in enumerate(articles, start=1):
        content_add = (f"{idx}  Title: {art['title']}" + f"Source {art.get('source', {}).get('name')}" + f"  URL : {art['url']}" + f"At: {art['publishedAt']}")
        content.append(content_add)
        print(f"{idx}. {art['title']}")
        print(f"   Source: {art.get('source', {}).get('name')}")
        print(f"   URL:    {art['url']}")
        print(f"   At:     {art['publishedAt']}\n")

    for entry in content:
        print (entry)