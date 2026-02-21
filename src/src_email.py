import os
import logging
from django.core.mail import EmailMessage
from django.contrib.auth.models import User

from dotenv import load_dotenv

load_dotenv()
ENV = os.getenv('ENV')
# to_email = os.getenv('TO_EMAIL')
from_email = os.getenv('FROM_EMAIL')

# Get admin email for CC
try:
    admin_user = User.objects.get(username='admin')
    admin_email = admin_user.email
except User.DoesNotExist:
    admin_email = None
    logger.warning("Admin user not found - CC email will not be used")

smtp_password = os.getenv('SMTP_PASSWORD')
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = from_email

# Configure logger
logger = logging.getLogger('src')


def send_email(subject, body, to_email, file_paths=None, is_html=False, cc_enabled=True):
    """
    Sends an email with the specified subject and body. Optionally attaches a file.

    Args:
        subject (str): The subject of the email.
        body (str): The body of the email.
        to_email (str): The recipient's email address.
        file_paths (list, optional): The paths to files to be attached. Defaults to None.
        is_html (bool, optional): Whether the email body is HTML. Defaults to False.
        cc_enabled (bool, optional): Whether to CC the admin email. Defaults to True.

    Raises:
        FileNotFoundError: If the file specified in file_path does not exist.
        Exception: If there is an error sending the email.

    Returns:
        None
    """
    logger.info(f"=== send_email() START ===")
    logger.info(f"Email subject: {subject}")
    logger.info(f"Recipient (to_email): {to_email}")
    logger.info(f"Sender (from_email): {from_email}")
    logger.info(f"CC email enabled: {cc_enabled}")
    if cc_enabled and admin_email:
        logger.info(f"CC address: {admin_email}")
    
    # Create email message using EmailMessage from django.core.mail
    cc_recipients = []
    if cc_enabled and admin_email:
        cc_recipients = [admin_email]
    
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=from_email,
        to=[to_email],
        cc=cc_recipients,
    )

    # Set content_subtype to 'html' if is_html is True
    if is_html:
        logger.debug("Email format: HTML")
        email.content_subtype = 'html'
    else:
        logger.debug("Email format: Plain text")

    if file_paths:
        logger.info(f"Files to attach: {len(file_paths)}")
        for idx, path in enumerate(file_paths, 1):
            try:
                if os.path.exists(path):
                    file_size = os.path.getsize(path)
                    logger.info(f"  Attachment {idx}: {os.path.basename(path)}")
                    logger.debug(f"    - Full path: {os.path.abspath(path)}")
                    logger.debug(f"    - File size: {file_size} bytes")
                    email.attach_file(path)
                else:
                    logger.warning(f"  ⚠ Attachment file not found: {path}")
            except Exception as e:
                logger.error(f"  ✗ Error attaching file {path}: {str(e)}", exc_info=True)

    try:
        email.send()
        logger.info(f"✓ Email sent successfully!")
        logger.info(f"  - To: {to_email}")
        logger.info(f"  - From: {from_email}")
        logger.info(f"  - Subject: {subject}")
        logger.info(f"=== send_email() END (SUCCESS) ===")
    except Exception as e:
        logger.error(f"✗ Failed to send email: {str(e)}", exc_info=True)
        logger.error(f"  - Recipient: {to_email}")
        logger.error(f"  - Sender: {from_email}")
        logger.error(f"  - Subject: {subject}")
        logger.info(f"=== send_email() END (FAILED) ===")
        raise

    if file_paths:
        logger.debug("Cleaning up attached files...")
        for path in file_paths:
            try:
                # Delete the files
                os.remove(path)
                logger.debug(f"✓ Deleted file: {path}")
            except Exception as e:
                logger.error(f"✗ Error deleting file {path}: {str(e)}", exc_info=True)


