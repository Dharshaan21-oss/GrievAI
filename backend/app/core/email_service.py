import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

def send_grievance_notification(to_email: str, grievance):
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        print(f"[EMAIL SKIPPED - no SMTP configured] Would notify {to_email} about grievance #{grievance.id}: {grievance.title}")
        return False

    if not to_email:
        print(f"[EMAIL SKIPPED - no recipient] Grievance #{grievance.id} has no department email on file")
        return False

    subject = f"New Grievance Assigned: #{grievance.id} - {grievance.title}"
    body = f"""
A new grievance has been routed to your department.

Grievance ID: #{grievance.id}
Title: {grievance.title}
Category: {grievance.category} ({round((grievance.category_confidence or 0) * 100)}% confidence)
Priority: {grievance.priority.value.upper()}
Location: {grievance.location or 'Not specified'}

Description:
{grievance.description}

AI Summary:
{grievance.ai_summary}

Please review this grievance in the GrievAI admin dashboard.
"""

    msg = MIMEMultipart()
    msg['From'] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_USER}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_USER, to_email, msg.as_string())
        server.quit()
        print(f"[EMAIL SENT] Notified {to_email} about grievance #{grievance.id}")
        return True
    except Exception as e:
        print(f"[EMAIL FAILED] Could not send to {to_email}: {e}")
        return False