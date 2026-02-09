import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_application_alert(recipient_email: str, candidate_name: str, job_title: str):
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; border: 1px solid #e2e8f0; padding: 20px; border-radius: 10px;">
            <h2 style="color: #2563eb;">New Job Application Received</h2>
            <p>Hello,</p>
            <p>You have received a new application for the position: <strong>{job_title}</strong>.</p>
            <hr style="border: 0; border-top: 1px solid #eee;">
            <p><strong>Candidate Details:</strong></p>
            <ul>
                <li><strong>Name:</strong> {candidate_name}</li>
            </ul>
            <p>Login to your OriginX Business dashboard to review the full details and resume.</p>
            <p style="margin-top: 30px; font-size: 0.8em; color: #64748b;">
                Best Regards,<br>
                OriginX Team
            </p>
        </div>
    </body>
    </html>
    """

    message = MessageSchema(
        subject=f"New Application: {job_title} - {candidate_name}",
        recipients=[recipient_email],
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    print(f"Email sent to {recipient_email}")
