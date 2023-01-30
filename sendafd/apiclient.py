"""
Fetch area forecast discussion text from the National Weather Service API and parse as needed. See
https://www.weather.gov/documentation/services-web-api for API docs.
"""

import requests
import logging

logger = logging.getLogger(__name__)