"""
Send an email via a SMTP server. Takes html or plain text from renderer.py as input.
"""

import smtplib
import logging

logger = logging.getLogger(__name__)