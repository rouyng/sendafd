"""
Send an email via a SMTP server. Takes html or plain text from renderer.py as input.
"""

import smtplib
import logging

logger = logging.getLogger(__name__)

def send_email(smtp_server: str,
               smtp_username: str,
               smtp_pw: str,
               recipient: str,
               email_body: str,
               smtp_port: int = 587):
    """Connect to SMTP server and send email to the destination address"""
    try:
        logger.debug(f"Connecting to SMTP server at {smtp_server}:{smtp_port}")
        smtp_connection  = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        logger.debug("Server connection appears successful")
    except smtplib.SMTPException:
        logger.exception("Connection to SMTP server failed", exc_info=True)
        return False
    try:
        logger.debug(f"Logging in to SMTP server as {smtp_username}")
        smtp_connection.starttls()
        smtp_connection.ehlo()
        smtp_connection.login(user=smtp_username,
                              password=smtp_pw)
        logger.debug("Login appears successful")
    except smtplib.SMTPAuthenticationError:
        logger.critical("Error logging in to SMTP server, check username and password", exc_info=True)
        return False
    except (smtplib.SMTPHeloError, smtplib.SMTPNotSupportedError):
        logger.critical("Error connecting using STARTTLS, email server may not support STARTTLS.", exc_info=True)
        return False
    except RuntimeError:
        logger.critical("SSL/TLS support not available to your Python interpreter, could not send email.")
        return False
    logger.debug(f"Sending email to {recipient}")
    sent_status = smtp_connection.sendmail(smtp_username, recipient, email_body)
    if len(sent_status) > 0:
        logger.critical(f"Email could not be delivered: {sent_status}")
        return False
    else:
        logger.debug(f"Email sent to {recipient}")
        return True
