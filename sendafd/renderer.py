"""
Renders email templates. Takes forecast text from apiclient.py as input and outputting html
or plaintext.
"""

from jinja2 import Environment, PackageLoader, select_autoescape
import logging
from . import apiclient

logger = logging.getLogger(__name__)

# create Jinja Environment
env = Environment(
    loader=PackageLoader("sendafd"),
    autoescape=select_autoescape()
)

def render_email(afd: apiclient.AreaForecastDiscussion, template_path: str = None):
    """Render email as plaintext or html using specified jinja template"""
    if template_path:
        template = env.get_template(template_path)
        return template.render() # TODO: pass variables to template
    else:
        logger.debug("No template path provided, generating plaintext email")
        subject_line = f"Subject: {afd.issuing_office} Forecast for " \
                               f"{afd.issuance_time.strftime('%D %H:%M')}\n"
        plaintext_email_body = subject_line + afd.raw_text
        return plaintext_email_body
