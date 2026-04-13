from resources.user import send_email

def send_email_task(to_email, subject):
    print("Worker sending email...")
    send_email(to_email, subject)