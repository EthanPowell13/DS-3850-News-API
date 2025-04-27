import json
import urllib.request
from datetime import date
from config import NEWS_API_KEY

def format_newsletter(topic: str, summaries: list) -> str:
    today = date.today().strftime("%B %d, %Y")

    prompt = (
        f"Create a clean, engaging email newsletter for the topic '{topic}' "
        f"on {today}. The content should be friendly, professional, and include bullet points. "
        f"Below are the article summaries:\n\n"
    )

    for idx, summary in enumerate(summaries, start=1):
        prompt += f"{idx}. {summary}\n\n"

    request_body = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.6
    }).encode("utf-8")

    req = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=request_body)
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {NEWS_API_KEY}")

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error formatting newsletter: {e}"