"""
Renders email templates. Takes forecast text from apiclient.py as input and outputting html
or plaintext.
"""

from email.message import EmailMessage
from jinja2 import Environment, PackageLoader, select_autoescape
import logging
from . import apiclient

logger = logging.getLogger(__name__)

# create Jinja Environment
env = Environment(
    loader=PackageLoader("sendafd"),
    autoescape=select_autoescape()
)

def build_email(afd: apiclient.AreaForecastDiscussion,
                sender_email: str,
                recipient_email: str,
                template_path: str = None) -> EmailMessage:
    """Construct an EmailMessage object from AreaForecastDiscussion, template and metadata"""
    msg = EmailMessage()
    body = render_email_body(afd, template_path)
    msg.set_content(body)
    msg['Subject'] = f"Subject: {afd.issuing_office} Forecast for " \
                               f"{afd.issuance_time.strftime('%D %H:%M')}"
    msg['From'] = sender_email
    msg['To'] = recipient_email
    return msg

def render_email_body(afd: apiclient.AreaForecastDiscussion, template_path: str = None):
    """Render email body as plaintext or html using specified jinja template"""
    if template_path:
        template = env.get_template(template_path)
        logger.debug(f"Rendering email body from template at: {template_path}")
        return template.render() # TODO: pass variables to template
    else:
        logger.debug("No template path provided, generating plaintext email")
        plaintext_email_body = afd.raw_text
        return plaintext_email_body
