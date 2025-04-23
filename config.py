from dotenv import load_dotenv
import os

load_dotenv()  # reads .env


NEWS_API_KEY = os.getenv("API_KEY")
if not NEWS_API_KEY:
    raise ValueError("Missing NEWS_API_KEY in .env")

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")