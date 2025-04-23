# emailer.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS

def send_newsletter(
    subject: str,
    html_body: str,
    recipients: List[str]
) -> None:
    """
    Send an HTML email to the list of recipients.
    """
    # Set up the SMTP server connection
    server = smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASS)

    for recipient in recipients:
        msg = MIMEMultipart("alternative")
        msg["From"] = SMTP_USER
        msg["To"] = recipient
        msg["Subject"] = subject

        # Plain-text fallback
        text_body = "This email contains HTML content. Please view it in an HTML-capable email client."
        part1 = MIMEText(text_body, "plain")
        part2 = MIMEText(html_body, "html")

        msg.attach(part1)
        msg.attach(part2)

        server.send_message(msg)
        print(f"Sent to {recipient}")

    server.quit()

if __name__ == "__main__":
    # Quick test
    test_recipients = ["ethanwpowell13@gmail.com"]
    test_subject = "📰 Test Newsletter"
    test_html = """
    <h1>Today's News</h1>
    <ul>
      <li><strong>Headline 1</strong><br/>Summary 1…</li>
      <li><strong>Headline 2</strong><br/>Summary 2…</li>
    </ul>
    """
    send_newsletter(test_subject, test_html, test_recipients)