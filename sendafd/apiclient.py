"""
Fetch area forecast discussion text from the National Weather Service API and parse as needed. See
https://www.weather.gov/documentation/services-web-api for API docs.
"""

import requests
import logging

logger = logging.getLogger(__name__)

def print_region_codes():
    """
    Query the NWS API for a list of valid region codes for area forecast discussion, then print
    the codes with descriptions.
    """
    endpoint_url = "https://api.weather.gov/products/types/AFD/locations"
    logging.debug(f"Checking for region codes using NWS API endpoint at {endpoint_url}")
    api_response = requests.get(endpoint_url)
    api_response.raise_for_status()
    logging.debug("NWS API request appears successful")
    for c, d in api_response.json()['locations'].items():
        print(c, d)

