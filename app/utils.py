from flask import session
from flask_mail import Message
from app import mail, app
from flask import current_app, url_for
from app.models import Product
from itsdangerous import URLSafeTimedSerializer
import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from app.config import Config

MAIL_USERNAME = Config.MAIL_USERNAME
MAIL_PASSWORD = Config.MAIL_PASSWORD
SMTP_SERVER = Config.MAIL_SERVER
SMTP_PORT = Config.MAIL_PORT
#SMTP_SERVER, SMTP_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD
EMAIL_ADDRESS = Config.MAIL_USERNAME
EMAIL_PASSWORD = Config.MAIL_PASSWORD

def calculate_cart_total():
    """Calculate the total price of items in the cart."""
    total = 0
    if 'cart' in session:
        for item in session['cart'].values():
            total += item['price'] * item['quantity']
    return total

def is_admin(user):
    """Check if the logged-in user is an admin."""
    return user.role == 'admin'

def is_vendor(user):
    """Check if the logged-in user is a vendor."""
    return user.role == 'vendor'

"""
def send_email(subject, recipient, body):
    msg = Message(subject, sender=MAIL_USERNAME, recipients=[recipient])
    msg.body = body
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False
"""

def send_order_confirmation(user_email, order_details):
    """Send an email confirmation after an order is placed."""
    subject = "Order Confirmation - Your Purchase Details"
    body = f"Thank you for your order!\n\nOrder Details:\n{order_details}"
    return send_email(subject, user_email, body)

def send_password_reset_email(user_email, reset_link):
    """Send a password reset email."""
    subject = "Password Reset Request"
    body = f"Click the link below to reset your password:\n\n{reset_link}"
    return send_email(subject, user_email, body)
    


def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=current_app.config["SECURITY_PASSWORD_SALT"])

def verify_reset_token(token, expiration=1800):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(token, salt=current_app.config["SECURITY_PASSWORD_SALT"], max_age=expiration)
        return email
    except:
        return None

def send_reset_email(email, token):
    reset_url = url_for('main.reset_password', token=token, _external=True)
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg['Subject'] = "Password Reset Request"
    msg.attach(MIMEText(f"Click the link to reset your password: {reset_url}\nIf you did not request this, ignore this email.", 'plain'))
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        print(f"Email sending failed: {e}")
    



def send_email(subject, receiver_email, body, cc_emails=None, bcc_emails=None, attachment_path=None):
    try:
        # Create Email Message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Add CC and BCC
        if cc_emails:
            msg['Cc'] = ', '.join(cc_emails)
        if bcc_emails:
            bcc_emails = bcc_emails
        else:
            bcc_emails = []

        # Attach email body (HTML or Plain Text)
        msg.attach(MIMEText(body, 'html'))

        # Use 'plain' for simple text emails
        # Attach a file if provided
        if attachment_path:
            filename = os.path.basename(attachment_path)
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={filename}")
                msg.attach(part)

        # Connect to SMTP Server
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            # Identifies itself to the SMTP server
            server.starttls(context=context)
            # Secure connection upgrade
            server.ehlo()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            # Login
            server.sendmail(EMAIL_ADDRESS, [receiver_email] + (cc_emails or []) + bcc_emails, msg.as_string())
            print("✅ Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication Error! Check your email and password.")
    except smtplib.SMTPConnectError:
        print("❌ Unable to connect to SMTP server.")
    except smtplib.SMTPRecipientsRefused:
        print("❌ Email address rejected by the server.")
    except Exception as e:
        print(f"❌ Error: {e}")
