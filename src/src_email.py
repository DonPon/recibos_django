import os
from django.core.mail import EmailMessage

from dotenv import load_dotenv

load_dotenv()
ENV = os.getenv('ENV')
# to_email = os.getenv('TO_EMAIL')
from_email = os.getenv('FROM_EMAIL')
cc_email = os.getenv('CC_EMAIL')
smtp_password = os.getenv('SMTP_PASSWORD')
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = from_email


def send_email(subject, body, to_email, file_paths=None):
    """
    Sends an email with the specified subject and body. Optionally attaches a file.

    Args:
        subject (str): The subject of the email.
        body (str): The body of the email.
        to_email (str): The recipient's email address.
        file_path (str, optional): The path to the file to be attached. Defaults to None.

    Raises:
        FileNotFoundError: If the file specified in file_path does not exist.
        Exception: If there is an error sending the email.

    Returns:
        None
    """
    # Create email message using EmailMessage from django.core.mail
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=from_email,
        to=[to_email],
        cc=[cc_email],
    )

    if file_paths:
        for path in file_paths:
            # attach a file (path or binary data)
            email.attach_file(path)

    email.send()

    
    if file_paths:
        for path in file_paths:
            # Delete the files
            # default_storage.delete(file_path)
            os.remove(path)


