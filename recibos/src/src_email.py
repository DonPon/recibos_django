import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders

from dotenv import load_dotenv

load_dotenv()
ENV = os.getenv('ENV')
to_email = os.getenv('TO_EMAIL')
from_email = os.getenv('FROM_EMAIL')
cc_email = os.getenv('CC_EMAIL')
smtp_password = os.getenv('SMTP_PASSWORD')
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = from_email



def send_email(subject,body,file_path=None):
    # Create a multipart message
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = to_email
    message['Cc'] = cc_email
    message.attach(MIMEText(body, 'plain'))


    if file_path:
        # Prepare attachement
        with open(file_path, 'rb') as f:
            file_content = f.read()

        # Create a MIMEApplication with the file content
        attachment = MIMEApplication(file_content, _subtype="pdf")

        # Extract the filename from the file path
        filename = file_path.split('/')[-1]  # Adjust this based on your file paths
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        
        # Attach the file to the email
        message.attach(attachment)

    # Wrap the message
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        recipients = [to_email, cc_email]
        server.sendmail(from_email, recipients, message.as_string())
    
    if file_path:
        # Delete the files
        # default_storage.delete(file_path)
        os.remove(file_path)


