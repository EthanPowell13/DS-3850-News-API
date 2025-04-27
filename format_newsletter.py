import json
import urllib.request
from datetime import date
from config import NEWS_API_KEY
from summarize import OPENAI_API_KEY



def format_newsletter(report: str, topic: str) -> str:

    AI_API_KEY = OPENAI_API_KEY

    today = date.today().strftime("%B %d, %Y")

    prompt = (
        f"Create a clean, engaging email newsletter for the topic '{topic}' "
        f"on {today}. The content should be friendly, professional, and include a brief summary. "
        f"Below are the compiled article summaries:\n\n"
        f"{report}\n"
        f"Write your response in html that can be embedded in an email"
        f"Be sure to make it look pretty, and include a header."
        f"Use 'Daily News by AI' as the heading"
    )

    request_body = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.6
    }).encode("utf-8")

    req = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=request_body)
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {AI_API_KEY}")


    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error formatting newsletter: {e}"
        