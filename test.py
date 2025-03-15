from app.utils import send_email

# 📤 Call function to send a test email
send_email(
    subject="Test Email - Nexora Industry 🎉",
    receiver_email="sarvarsingh496@gmail.com",
    body="<h2>Hello Sarvar!</h2><p>This is a test email from Nexora Industry.</p>",
    cc_emails=["cc@example.com"],  # Optional CC
    bcc_emails=["bcc@example.com"],  # Optional BCC
    attachment_path=None  # Optional attachment
)
