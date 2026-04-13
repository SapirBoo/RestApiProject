from celery_app import celery
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

@celery.task
def send_email_task(to_email, subject):
    print("Send email..")
    message = Mail(
        from_email=os.getenv("FROM_EMAIL"),
        to_emails=to_email,
        subject=subject,
        plain_text_content="Welcome! You registered successfully."
    )

    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        return response.status_code

    except Exception as e:
        return str(e)
