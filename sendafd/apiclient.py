"""
Fetch area forecast discussion text from the National Weather Service API and parse as needed. See
https://www.weather.gov/documentation/services-web-api for API docs.
"""

import requests
import logging

logger = logging.getLogger(__name__)

def get_region_codes() -> dict:
    """
    Query the NWS API for a list of valid region codes for area forecast discussion and return as a
    dictionary.
    """
    endpoint_url = "https://api.weather.gov/products/types/AFD/locations"
    logger.debug(f"Checking for region codes using NWS API endpoint at {endpoint_url}")
    api_response = requests.get(endpoint_url)
    api_response.raise_for_status()
    logger.debug("NWS API request appears successful")
    return api_response.json()['locations']

def print_region_codes(codes: dict):
    """Print region codes"""
    for c, d in codes.items():
        print(c, d)

def fetch_afd(region: str, monitor: bool=False) -> dict:
    """
    Query the NWS API for the area forecast discussions for the supplied region code, then return
    the API response with the latest AFD.
    """
    # check supplied region code is valid by checking against valid codes provided by the NWS API
    valid_codes = get_region_codes()
    if region.lower() not in [code.lower() for code in valid_codes.keys()]:
        logger.critical(f"'{region}' is not a valid region code. Please use one of the following:")
        print_region_codes(valid_codes)
        return {'response': None, 'error': "Invalid region code"}
    else:
        logger.debug(f"Getting list of published AFDs for region {region}")
        # get the list of recently issued AFDs for the supplied region code
        afd_list_response = requests.get(f"https://api.weather.gov/products/types/afd/locations/{region.lower()}")
        try:
            afd_list_response.raise_for_status()
        except requests.HTTPError:
            logger.exception("HTTP error fetching list of AFD products")
            return {'response': None, 'error': "HTTP error fetching list of AFD products"}
        try:
            # from the list, grab the product ID of tge latest issued AFD
            logger.debug(f"Returned {len(afd_list_response.json()['@graph'])} AFDs")
            latest_product_id = afd_list_response.json()['@graph'][0]['id']
            logger.debug(f"Latest AFD product ID: {latest_product_id}, issued {afd_list_response.json()['@graph'][0]['issuanceTime']}")
        except KeyError:
            logger.exception("Unexpected API response structure")
            return {'response': None, 'error': "Unexpected API response structure"}
        if monitor:
            # TODO: check latest product ID against cached product ID and see if it has changed.
            #  If it hasn't, don't fetch the full AFD and exit.
            cached_id = "foo" # placeholder value
            if latest_product_id == cached_id:
                logger.debug(f"Latest product had same id ({latest_product_id}) as cached product ({cached_id}), ignoring.")
                return {'response': None, 'error': None}
            else:
                logger.debug(
                    f"Latest product had different id ({latest_product_id}) than cached product ({cached_id}), fetching latest product...")
        afd_product_response = requests.get(f"https://api.weather.gov/products/{latest_product_id}")
        try:
            afd_product_response.raise_for_status()
            return {'response': afd_product_response.json(), 'error': None}
        except requests.HTTPError:
            logger.exception("HTTP error fetching AFD product")
            error_description = "HTTP error fetching AFD product"
            return {'response': None, 'error': "HTTP error fetching AFD product"}

