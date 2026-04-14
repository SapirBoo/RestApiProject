from celery_app import celery
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To
import os

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
TEMPLATE_ID = os.getenv("TEMPLATE_ID")

@celery.task
def send_verification_email(to_email: str, name: str,token: str):
    message = Mail(
    from_email=os.getenv("FROM_EMAIL"),
    to_emails=To(to_email),
    )

    verification_link: f"https://restful-api-python-project.onrender.com/verify?token={token}"
    
    message.dynamic_template_data = {
    "name": name,
    "email": to_email,
    "verification_link": verification_link
    }

    message.template_id = str(TEMPLATE_ID)    
    
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        return response.status_code

    except Exception as e:
        return str(e)
