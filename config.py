from dotenv import load_dotenv
import os

load_dotenv()  # reads .env

#API_KEY = '33a48badff5143a69cdcf29a31e931f2'
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
if not NEWS_API_KEY:
    raise ValueError("Missing NEWS_API_KEY in .env")