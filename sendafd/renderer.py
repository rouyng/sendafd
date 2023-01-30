"""
Renders email templates. Takes forecast text from apiclient.py as input and outputting html
or plaintext.
"""

import jinja2
import logging

logger = logging.getLogger(__name__)