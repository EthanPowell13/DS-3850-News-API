# summarize.py
import os
from openai import OpenAI
from typing import Dict
import json
from config import NEWS_API_KEY

import urllib.request
from dotenv import load_dotenv
import os

load_dotenv()  # reads .env
article_keyword = 'stocks'
email_subject = "📰 Daily Newsletter"
email_recipients = ["ethanwpowell13@gmail.com", "sewells43@tntech.edu"] 

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def summarize_article(
    title: str,
    url: str,
    content: str,
    max_tokens: int = 150
) -> str:
    """
    Summarize `content` of a news article into a concise, email‑friendly summary.
    Returns a plain-text string (e.g., 2–3 bullet points).
    """
    prompt = (
        f"Include the article title and author before your summary, Summarize the following news article for a quick email newsletter. "
        f"Title: {title}\nURL: {url}\n\n"
        f"Article content:\n{content}\n\n"
        "Provide 2–3 bullet points that capture the main points clearly and concisely."
    )
    client = OpenAI(api_key = OPENAI_API_KEY)
    data = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }).encode("utf-8")

    req = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=data)
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {OPENAI_API_KEY}")

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {e}"
    # Extract and return the assistant’s reply

if __name__ == "__main__":
    # Quick test with fetched article
    from fetch import fetch_articles

    articles = fetch_articles(article_keyword, max_results=5)
    test_query = article_keyword
    print(f"Fetching top 5 articles for: {test_query!r}\n")
    report_compile = ""
    for idx, art in enumerate(articles, start=1):

        content = art.get('content', 'No content available')
        title = f"{art['title']}"
        source = f"   Source: {art.get('source', {}).get('name')}"  
        url = f"   URL:    {art['url']}"
        author =art.get('Author', 'Unknown Author')
        publishedAt = f"   At:     {art['publishedAt']}\n"

        '''
        print(f"{idx}. {art['title']}")
        print(content)
        print(f"   Source: {art.get('source', {}).get('name')}")
        print(f"   URL:    {art['url']}")
        print(f"   At:     {art['publishedAt']}\n")
        '''

        summary = summarize_article(
            title,
            url,
            content
        )
        entry = (
            f"{idx}. Title: {title}\n"
            f"Author: {author}\n"
            f"Summary:\n{summary}\n"
            "-------------------------\n"
        )
        report_compile += entry

    #print("\n=== Articles ===\n")
    #print(report_compile)

    from format_newsletter import format_newsletter
    from emailer import send_newsletter

    newsletter_html = format_newsletter(report_compile, article_keyword)

    send_newsletter(email_subject,newsletter_html, email_recipients)