"""
Renders email templates. Takes forecast text from apiclient.py as input and outputting html
or plaintext.
"""

from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader, select_autoescape
import logging
from . import apiclient

logger = logging.getLogger(__name__)

# create Jinja Environment
env = Environment(
    loader=FileSystemLoader('templates/'),
    autoescape=select_autoescape()
)

def build_email(afd: apiclient.AreaForecastDiscussion,
                sender_email: str,
                recipient_email: str,
                template_path: str = None) -> EmailMessage:
    """Construct an EmailMessage object from AreaForecastDiscussion, template and metadata"""
    msg = EmailMessage()
    plaintext_body = afd.raw_text
    msg.set_content(plaintext_body)
    if template_path:
        # create a multipart message, including plaintext and html
        html_body = render_email_body(afd, template_path)
        msg.add_alternative(html_body, subtype='html')
    else:
        logger.debug("No template path provided, generating plaintext email")
    msg['Subject'] = f"{afd.issuing_office} Forecast for {afd.issuance_time.strftime('%D %H:%M')}"
    msg['From'] = sender_email
    msg['To'] = recipient_email
    return msg

def render_email_body(parsed_afd: apiclient.AreaForecastDiscussion, template_path: str) -> str:
    """Render email body as plaintext or html using specified jinja template"""
    template = env.get_template(template_path)
    logger.debug(f"Rendering email body from template at: {template_path}")
    return template.render(afd=parsed_afd)

