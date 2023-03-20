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
    codes_with_description = api_response.json()['locations']
    if len(codes_with_description) == 0:
        logger.error(f"Request was successful, but zero location codes were received."
                        f"\n Response headers: {api_response.headers}")
        raise ValueError
    else:
        logger.debug("NWS API request appears successful")
        return api_response.json()['locations']

def print_region_codes(codes: dict):
    """Print region codes"""
    for c, d in codes.items():
        print(c, d)

def fetch_afd(region: str, monitor: bool=False, ignore_region_validation: bool=True) -> dict:
    """
    Query the NWS API for the area forecast discussions for the supplied region code, then return
    the API response with the latest AFD.
    """
    # check supplied region code is valid by checking against valid codes provided by the NWS API
    region_lc = region.lower()
    if not ignore_region_validation:
        try:
            valid_codes = get_region_codes()
            if region_lc not in [code.lower() for code in valid_codes.keys()]:
                logger.critical(
                    f"'{region}' is not a valid region code. Please use one of the following:")
                print_region_codes(valid_codes)
                return {'response': None, 'error': "Invalid region code"}
        except requests.HTTPError:
            logger.exception("HTTP error fetching list of region codes")
            return {'response': None, 'error': "HTTP error fetching list of region codes"}
        except ValueError:
            return {'response': None, 'error': "Could not validate region code"}
    logger.debug(f"Getting list of published AFDs for region {region}")
    # get the list of recently issued AFDs for the supplied region code
    afd_list_response = requests.get(f"https://api.weather.gov/products/types/afd/locations/{region_lc}")
    try:
        afd_list_response.raise_for_status()
    except requests.HTTPError:
        logger.exception("HTTP error fetching list of AFD products")
        return {'response': None, 'error': "HTTP error fetching list of AFD products"}
    try:
        # from the list, grab the product ID of the latest issued AFD
        logger.debug(f"Returned {len(afd_list_response.json()['@graph'])} AFDs")
        latest_product_id = afd_list_response.json()['@graph'][0]['id']
        logger.debug(f"Latest AFD product ID: {latest_product_id}, issued {afd_list_response.json()['@graph'][0]['issuanceTime']}")
    except KeyError:
        logger.exception("Unexpected API response structure")
        return {'response': None, 'error': "Unexpected API response structure"}
    if monitor:
        cached_afd = read_afd_cache(cache_path=f"cache_{region_lc}.json")
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
            create_afd_cache(afd_product_response.json(), cache_path=f"cache_{region_lc}.json")
        return {'response': afd_product_response.json(), 'error': None}
    except requests.HTTPError:
        logger.exception("HTTP error fetching AFD product")
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


class AreaForecastDiscussion:
    """
    Take the raw AFD product returned by the NWS API and parse the metadata and product body text
    into an object ready to be consumed by the renderer.
    """
    def __init__(self, raw_afd: dict):
        """

        :param raw_afd: dictionary containing raw AFD product, in the same format returned by the
        NWS API
        """
        self.product_id = raw_afd['id']
        self.issuing_office = raw_afd['issuingOffice']
        self.issuance_time = datetime.strptime(raw_afd['issuanceTime'], "%Y-%m-%dT%H:%M:%S%z")
        self.raw_text = raw_afd['productText']
        # remove extra newlines
        self.cleaned_text = self.clean_newlines(self.raw_text)
        # separate out sections using '&&' to demarcate
        raw_sections = [s.strip() for s in self.cleaned_text.split("&&")]
        # parse header and footer sections first to preserve ordering
        self.sections = [self.Section(raw_sections.pop(0), "header"),
                         self.Section(raw_sections.pop(), "footer")]
        # parse the rest of the sections, putting them in order between header and footer
        for s in raw_sections:
            self.sections.insert(len(self.sections) - 1, self.Section(s))
        # initialize named sections from section list
        self.header = self.sections[0].body
        self.footer = self.sections[-1].body
        for s in self.sections[1:-1]:
            name_lc = s.name.lower()
            translate_table = name_lc.maketrans({' ' : '_',
                                                 '/': '_',
                                                 '-': '_',
                                                 '(': '',
                                                 ')': ''})
            attr_name = name_lc.translate(translate_table)
            setattr(self, attr_name, s.body)



    class Section:
        section_header_regex = re.compile("\.(.*?)\.\.\. ")
        def __init__(self, raw_section: str, name: str=None):
            if name is not None:
                self.name =  name
                self.body = raw_section.strip()
            else:
                section_header_match = re.match(self.section_header_regex, raw_section)
                if section_header_match:
                    self.name = section_header_match[1].title().strip()
                    headerless_body = raw_section.lstrip(section_header_match[0])
                    self.body = headerless_body.strip()
                else:
                    self.name = 'unnamed'
                    self.body = raw_section.strip()
            self.subsections: list = []
            subsection_match = re.search(self.section_header_regex, self.body)
            if subsection_match:
                subsections_raw = self.body[subsection_match.start():]
                self.body = self.body[:subsection_match.start()]
                ungrouped_header_regex = re.compile("\..*?\.\.\.")
                subsection_match = re.findall(ungrouped_header_regex, subsections_raw)
                for n, match in enumerate(subsection_match):
                    subsection_start = subsections_raw.find(match)
                    try:
                        subsection_end = subsections_raw.find(subsection_match[n+1])
                        self.subsections.append(
                            self.Subsection(subsections_raw[subsection_start:subsection_end]))
                    except IndexError:
                        self.subsections.append(self.Subsection(subsections_raw[subsection_start:]))

        class Subsection:
            subsection_header_regex = re.compile("\.(.*?)\.\.\.")
            def __init__(self, raw_subsection: str):
                subsection_header_match = re.match(self.subsection_header_regex, raw_subsection)
                self.name = subsection_header_match[1].title().strip()
                headerless_body = raw_subsection.lstrip(subsection_header_match[0])
                self.body = headerless_body.strip()

    @staticmethod
    def clean_newlines(raw_text: str) -> str:
        """Parse raw NWS AFD product text, removing newline characters used for layout
        purposes in the original text and replacing double newlines used for paragraph
        breaks with single newlines"""
        paragraphs = raw_text.split("\n\n")
        cleaned_paragraphs = []
        for p in paragraphs:
            removed_newlines = p.replace("\n", " ")
            removed_doublespace = removed_newlines.replace("  ", " ")
            cleaned_paragraphs.append(removed_doublespace.strip())
        return "\n".join(cleaned_paragraphs)



