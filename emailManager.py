import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pytz

from payloadCollection import PayloadCollection



def send_email(
    subject,
    message,
):
    # Email configuration
    from_email = PayloadCollection.email_user
    password = PayloadCollection.email_pass
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    starttls = True
    username = PayloadCollection.email_user
    to_email = ["ramzi.d@outlook.com", "rdr@einbruchschutz.ch"]

    # Create a MIMEText object to represent the email message
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = ", ".join(to_email)
    msg["Subject"] = f"From Cannerald eventServer:{subject} "
    msg.attach(MIMEText(message, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        if starttls:
            server.starttls()
        server.login(username, password)

        for recipient in to_email:
            server.sendmail(from_email, recipient.strip(), msg.as_string())

        # Close the connection
        server.quit()

     #   print("Email sent successfully.")
    except Exception as e:
        print("Error sending email:", str(e))
