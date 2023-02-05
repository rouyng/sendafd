"""
Fetch area forecast discussion text from the National Weather Service API and parse as needed. See
https://www.weather.gov/documentation/services-web-api for API docs.
"""

from datetime import datetime
import json
import re
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
            cached_afd = read_afd_cache()
            try:
                cached_id = cached_afd['id']
            except KeyError:
                cached_id = None
            if latest_product_id == cached_id:
                logger.debug(f"Latest product had same id ({latest_product_id}) as cached product ({cached_id}), ignoring.")
                return {'response': None, 'error': None}
            else:
                logger.debug(
                    f"Latest product had different id ({latest_product_id}) than cached product ({cached_id}), fetching latest product...")
        afd_product_response = requests.get(f"https://api.weather.gov/products/{latest_product_id}")
        try:
            afd_product_response.raise_for_status()
            if monitor:
                create_afd_cache(afd_product_response.json())
            return {'response': afd_product_response.json(), 'error': None}
        except requests.HTTPError:
            logger.exception("HTTP error fetching AFD product")
            error_description = "HTTP error fetching AFD product"
            return {'response': None, 'error': "HTTP error fetching AFD product"}

def create_afd_cache(afd_raw: dict, cache_path: str = "cache.json"):
    """
    Serialize as JSON a dictionary containing the raw AFD product, then write it to a file.

    :param afd_raw:
    :param cache_path:
    :return:
    """
    logger.debug(f"Writing cache file at {cache_path}")
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(afd_raw, f, ensure_ascii=False, indent=4)

def read_afd_cache(cache_path: str = "cache.json") -> dict:
    """
    Read json file containing afd cache and return as a dictionary.

    :param cache_path: Path to cache file, defaults to "cache.json"
    :return: Dict containing AFD product
    """
    logger.debug(f"Reading cache file at {cache_path}")
    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            cache_dict = json.load(f)
    except FileNotFoundError:
        logger.warning(f"Cache file not found at {cache_path}")
        cache_dict = {}
    return cache_dict

def parse_raw_afd(raw_afd: dict) -> dict:
    """
    Take the raw AFD product returned by the NWS API and parse the metadata and product body text
    into a dictionary ready to be consumed by the renderer.

    :param raw_afd: dictionary containing raw AFD product
    :return: dictionary
    """
    product_id = raw_afd['id']
    issuing_office = raw_afd['issuingOffice']
    issuance_time = datetime.strptime(raw_afd['issuanceTime'], "%Y-%m-%dT%H:%M:%S%z")
    raw_sections = [s.strip() for s in raw_afd['productText'].split("&&")]
    sections = [{'name': 'Header', 'body': raw_sections.pop(0)},
                {'name': 'Credits', 'body': raw_sections.pop()}]
    section_header_regex = re.compile("\.(.+)\.\.\.")
    for s in raw_sections:
        section_header_match = re.match(section_header_regex, s)
        if section_header_match:
            header = section_header_match[1].capitalize()
            body = s.lstrip(section_header_match[0])
            sections.insert(len(sections)-1, {'name' : header, 'body' : body})
    return {
        'product id': product_id,
        'issuing office': issuing_office,
        'issuance time': issuance_time,
        'sections' : sections
    }