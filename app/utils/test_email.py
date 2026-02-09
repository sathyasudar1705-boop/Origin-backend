import asyncio
import os
import sys

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.utils.email import send_application_alert
from app.core.config import settings

async def test_email():
    print("--- OriginX Email Test Script ---")
    print(f"Server: {settings.MAIL_SERVER}")
    print(f"From: {settings.MAIL_FROM}")
    
    recipient = input("Enter a recipient email address to test: ")
    candidate = "Test Candidate"
    job = "Software Engineer (Internal Test)"
    
    print(f"Sending test email to {recipient}...")
    try:
        await send_application_alert(recipient, candidate, job)
        print("Success! Please check your inbox.")
    except Exception as e:
        print(f"Failed to send email: {e}")
        print("\nPossible reasons:")
        print("1. Incorrect SMTP credentials in .env")
        print("2. Gmail 'Less Secure Apps' is off or App Password is not used")
        print("3. Network/Firewall blocking SMTP port 587")

if __name__ == "__main__":
    asyncio.run(test_email())
