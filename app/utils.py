from flask import session, url_for, current_app
from flask_mail import Message
from app import mail
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
EMAIL_ADDRESS = Config.MAIL_USERNAME
EMAIL_PASSWORD = Config.MAIL_PASSWORD

# ✅ Calculate Total Cart Price
def calculate_cart_total():
    total = 0
    if 'cart' in session:
        for item in session['cart'].values():
            total += item['price'] * item['quantity']
    return total

# ✅ Role Checks
def is_admin(user):
    return user.role == 'admin'

def is_vendor(user):
    return user.role == 'vendor'

# ✅ Generate Secure Token
def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=current_app.config["SECURITY_PASSWORD_SALT"])

# ✅ Verify Reset Token
def verify_reset_token(token, expiration=1800):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(token, salt=current_app.config["SECURITY_PASSWORD_SALT"], max_age=expiration)
        return email
    except:
        return None

# ✅ Order Confirmation Email with Nexora Branding
def send_order_confirmation(user_email, order_details):
    subject = "🛍️ Order Confirmation - Nexora Industry"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);">
            <h2 style="color: #2E86C1; text-align: center;">Nexora Industry</h2>
            <h3 style="color: #28a745; text-align: center;">🎉 Your Order is Confirmed!</h3>
            <p style="font-size: 16px; color: #333;">Hello,</p>
            <p style="font-size: 16px; color: #333;">Thank you for shopping with <b>Nexora Industry</b>. Below are your order details:</p>
            <pre style="background: #f8f9fa; padding: 15px; border-radius: 5px; font-size: 14px; color: #333;">{order_details}</pre>
            <p style="font-size: 16px; color: #333;">We appreciate your business and look forward to serving you again! 🚀</p>
            <hr>
            <p style="font-size: 14px; text-align: center; color: #777;">This is an automated email from Nexora Industry.</p>
        </div>
    </body>
    </html>
    """
    return send_email(subject, user_email, body)

# ✅ Password Reset Email with Nexora Branding
def send_password_reset_email(user_email, reset_link):
    subject = "🔐 Password Reset Request - Nexora Industry"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);">
            <h2 style="color: #2E86C1; text-align: center;">Nexora Industry</h2>
            <h3 style="color: #d9534f; text-align: center;">🔑 Reset Your Password</h3>
            <p style="font-size: 16px; color: #333;">We received a request to reset your password.</p>
            <p style="font-size: 16px; color: #333;">Click the button below to set a new password:</p>
            <div style="text-align: center;">
                <a href="{reset_link}" style="background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-size: 16px;">Reset Password</a>
            </div>
            <p style="font-size: 14px; color: #777; text-align: center;">If you did not request this, you can ignore this email.</p>
            <hr>
            <p style="font-size: 14px; text-align: center; color: #777;">This is an automated email from Nexora Industry.</p>
        </div>
    </body>
    </html>
    """
    return send_email(subject, user_email, body)


def send_reset_email(email, token):
    reset_url = url_for('main.reset_password', token=token, _external=True)
    
    subject = "🔐 Password Reset Request - Nexora Industry"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);">
            <h2 style="color: #2E86C1; text-align: center;">Nexora Industry</h2>
            <h3 style="color: #d9534f; text-align: center;">🔑 Reset Your Password</h3>
            <p style="font-size: 16px; color: #333;">We received a request to reset your password.</p>
            <p style="font-size: 16px; color: #333;">Click the button below to set a new password:</p>
            <div style="text-align: center; margin: 20px;">
                <a href="{reset_url}" style="background-color: #28a745; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-size: 16px; display: inline-block;">Reset Password</a>
            </div>
            <p style="font-size: 14px; color: #777; text-align: center;">If you did not request this, you can ignore this email.</p>
            <hr>
            <p style="font-size: 14px; text-align: center; color: #777;">This is an automated email from Nexora Industry.</p>
        </div>
    </body>
    </html>
    """

    return send_email(subject, email, body)
        
        
# ✅ Send Email with HTML, Attachments, and Error Handling
def send_email(subject, receiver_email, body, cc_emails=None, bcc_emails=None, attachment_path=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = receiver_email
        msg['Subject'] = subject

        if cc_emails:
            msg['Cc'] = ', '.join(cc_emails)
        if bcc_emails:
            bcc_emails = bcc_emails
        else:
            bcc_emails = []

        msg.attach(MIMEText(body, 'html'))  # Attach HTML body

        if attachment_path:
            filename = os.path.basename(attachment_path)
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={filename}")
                msg.attach(part)

        # SMTP Connection & Sending Email
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
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