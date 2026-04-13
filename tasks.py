from celery_app import celery
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To
import os

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
TEMPLATE_ID = os.getenv("TEMPLATE_ID")

print("TEMPLATE_ID ENV:", os.getenv("TEMPLATE_ID"))
print("SENDGRID_TEMPLATE_ID ENV:", os.getenv("SENDGRID_TEMPLATE_ID"))

@celery.task
def send_email_task(to_email, subject):
    print("Send email..")
    message = Mail(
        from_email=os.getenv("FROM_EMAIL"),
        to_emails=to_email,
        subject=subject,
        plain_text_content="Welcome! You registered successfully."
    )
    
@celery.task
def send_welcome_email(to_email: str, name: str):
    
    message = Mail(
    from_email=os.getenv("FROM_EMAIL"),
    to_emails=To(to_email),
    )

    message.dynamic_template_data = {
    "name": name,
    "email": to_email
    }

    message.template_id = str(TEMPLATE_ID)    
    
    print(message.template_id)
    print(message.dynamic_template_data)
    
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        return response.status_code

    except Exception as e:
        return str(e)
