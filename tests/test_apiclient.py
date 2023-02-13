"""Test sendafd.apiclient module"""
import json

import pytest
import apiclient
from unittest.mock import Mock

import requests


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self):
            if args[0] == 'https://api.weather.gov/products/types/afd/locations/err':
                raise requests.HTTPError
            else:
                pass

    # response for testing product endpoint returning 500 error
    if args[0] == 'https://api.weather.gov/products/types/afd/locations/err':
        return MockResponse({
            "type": "urn:noaa:nws:api:UnexpectedProblem",
            "title": "Unexpected Problem",
            "status": 500,
            "detail": "An unexpected problem has occurred.",
            "instance": "urn:noaa:nws:api:request:493c3a1d-f87e-407f-ae2c-24483f5aab63",
            "correlationId": "493c3a1d-f87e-407f-ae2c-24483f5aab63",
            "additionalProp1": {}
        }, 500)
    # response for location list
    elif args[0] == "https://api.weather.gov/products/types/afd/locations":
        return MockResponse({
            "@context": [],
            "locations": {
                "ABQ": "Albuquerque, NM",
                "ABR": "Aberdeen, SD",
                "AFC": "Anchorage, AK",
                "AFG": "Fairbanks, AK",
                "AJK": "Juneau, AK",
                "AKQ": "Wakefield, VA",
                "ALY": "Albany, NY",
                "AMA": "Amarillo, TX",
                "APX": "Gaylord, MI",
                "ARX": "La Crosse, WI",
                "BGM": "Binghamton, NY",
                "BIS": "Bismarck, ND",
                "BMX": "NWS Birmingham, Alabama",
                "BOI": "Boise, ID",
                "BOU": "Denver/Boulder, CO",
                "BOX": "Boston / Norton, MA",
                "BRO": "Brownsville/Rio Grande Valley, TX",
                "BTV": "Burlington, VT",
                "BUF": "Buffalo, NY",
                "BYZ": "Billings, MT",
                "CAE": "Columbia, SC",
                "CAR": "Caribou, ME",
                "CHS": "Charleston, SC",
                "CLE": "Cleveland, OH",
                "CRP": "Corpus Christi, TX",
                "CTP": "State College, PA",
                "CYS": "Cheyenne, WY",
                "DDC": "Dodge City, KS",
                "DLH": "Duluth, MN",
                "DMX": "Des Moines, IA",
                "DTX": "Detroit/Pontiac, MI",
                "DVN": "Quad Cities, IA/IL",
                "EAX": "Kansas City/Pleasant Hill, MO",
                "EKA": "Eureka, CA",
                "EPZ": "El Paso, TX",
                "ERR": "Fake region for testing API error handling, does not exist in real NWS API",
                "EWX": "Austin/San Antonio, TX",
                "FFC": "Peachtree City, GA",
                "FGF": "Grand Forks, ND",
                "FGZ": "Flagstaff, AZ",
                "FSD": "Sioux Falls, SD",
                "FWD": "Fort Worth/Dallas, TX",
                "GGW": "Glasgow, MT",
                "GID": "Hastings, NE",
                "GJT": "Grand Junction, CO",
                "GLD": "Goodland, KS",
                "GRB": "Green Bay, WI",
                "GRR": "Grand Rapids, MI",
                "GSP": "Greenville-Spartanburg, SC",
                "GUM": "Tiyan, GU",
                "GYX": "Gray - Portland, ME",
                "HFO": "Honolulu, HI",
                "HGX": "Houston/Galveston, TX",
                "HNX": "San Joaquin Valley, CA",
                "HUN": "Huntsville, AL",
                "ICT": "Wichita, Kansas",
                "ILM": "NWS Wilmington, NC",
                "ILN": "Wilmington, OH",
                "ILX": "Central Illinois",
                "IND": "Indianapolis, IN",
                "IWX": "Northern Indiana",
                "JAN": "Jackson, Mississippi",
                "JAX": "Jacksonville, FL",
                "JKL": "Jackson, KY",
                "KEY": "Key West, FL",
                "LBF": "North Platte, NE",
                "LCH": "Lake Charles, LA",
                "LIX": "New Orleans/Baton Rouge",
                "LKN": "Elko, NV",
                "LMK": "Louisville, KY",
                "LOT": "Chicago, IL",
                "LOX": "Los Angeles, CA",
                "LSX": "St. Louis, MO",
                "LUB": "Lubbock, TX",
                "LWX": "Baltimore/Washington",
                "LZK": "Little Rock, AR",
                "MAF": "Midland/Odessa",
                "MEG": "Memphis, TN",
                "MFL": "Miami - South Florida",
                "MFR": "Medford, OR",
                "MHX": "Newport/Morehead City, NC",
                "MKX": "Milwaukee/Sullivan, WI",
                "MLB": "Melbourne, FL",
                "MOB": "Mobile/Pensacola",
                "MPX": "Twin Cities, MN",
                "MQT": "Marquette, MI",
                "MRX": "Morristown, TN",
                "MSO": "Missoula, MT",
                "MTR": "San Francisco Bay Area, CA",
                "OAX": "Omaha/Valley, NE",
                "OHX": "Nashville, TN",
                "OKX": "New York, NY",
                "OTX": "Spokane, WA",
                "OUN": "Norman, OK",
                "PAH": "Paducah, KY",
                "PBZ": "Pittsburgh, PA",
                "PDT": "Pendleton, OR",
                "PHI": "Philadelphia/Mt Holly",
                "PIH": "Pocatello, ID",
                "PPG": "WSO Pago Pago",
                "PQR": "Portland, OR",
                "PSR": "NWS Phoenix",
                "PUB": "Pueblo, CO",
                "RAH": "Raleigh, NC",
                "REV": "Reno, NV",
                "RIW": "Western and Central Wyoming",
                "RLX": "Charleston, WV",
                "RNK": "Blacksburg, VA",
                "SEW": "Seattle/Tacoma, WA",
                "SGF": "Springfield, MO",
                "SGX": "San Diego, CA",
                "SHV": "Shreveport, LA",
                "SJT": "San Angelo, TX",
                "SJU": "San Juan, PR",
                "SLC": "Salt Lake City, UT",
                "STO": "Sacramento, CA",
                "TAE": "Tallahassee, FL",
                "TBW": "Tampa Bay Area, FL",
                "TFX": "Great Falls, MT",
                "TOP": "Topeka, KS",
                "TSA": "Tulsa, OK",
                "TWC": "NWS Tucson Arizona",
                "UNR": "Rapid City, SD",
                "VEF": "Las Vegas, NV"
            }
        }, 200)
    # response for AFD list for region PSR
    elif args[0] == "https://api.weather.gov/products/types/afd/locations/psr":
        with open("psr_afd_list_response.json", 'r', encoding='utf-8') as f:
            json_response = json.load(f)
        return MockResponse(json_response, 200)
    # response for AFD list for region TOP
    elif args[0] == "https://api.weather.gov/products/types/afd/locations/top":
        with open("top_afd_list_response.json", 'r', encoding='utf-8') as f:
            json_response = json.load(f)
        return MockResponse(json_response, 200)
    # response for AFD list for region LOX
    elif args[0] == "https://api.weather.gov/products/types/afd/locations/lox":
        with open("lox_afd_list_response.json", 'r', encoding='utf-8') as f:
            json_response = json.load(f)
        return MockResponse(json_response, 200)
    # response for AFD list for region OKX
    elif args[0] == "https://api.weather.gov/products/types/afd/locations/okx":
        with open("okx_afd_list_response.json", 'r', encoding='utf-8') as f:
            json_response = json.load(f)
        return MockResponse(json_response, 200)
    # response for single AFD product for region PSR
    elif args[0] == "https://api.weather.gov/products/1d6cd33d-4017-4dd1-8dce-41d4541de35a":
        with open("psr_afd_response.json", 'r', encoding='utf-8') as f:
            json_response = json.load(f)
        return MockResponse(json_response, 200)
    # response for single AFD product for region TOP
    elif args[0] == "https://api.weather.gov/products/1f29f93c-583b-4144-ae22-8624a5e56504":
        with open("top_afd_response.json", 'r', encoding='utf-8') as f:
            json_response = json.load(f)
        return MockResponse(json_response, 200)
    # response for single AFD product for region LOX
    elif args[0] == "https://api.weather.gov/products/a922a688-acb5-4bb8-8a22-55c6a107b61d":
        with open("lox_afd_response.json", 'r', encoding='utf-8') as f:
            json_response = json.load(f)
        return MockResponse(json_response, 200)
    # response for single AFD product for region OKX
    elif args[0] == "https://api.weather.gov/products/6893e2af-17ef-471a-b7bc-4a74a8af0374":
        with open("okx_afd_response.json", 'r', encoding='utf-8') as f:
            json_response = json.load(f)
        return MockResponse(json_response, 200)
    return MockResponse(None, 404)


def mocked_requests_get_500(*args, **kwargs):
    """Mock for requests.get that always returns a 500 error code and associated API response"""
    class MockResponse:
        def __init__(self):
            self.json_data = {
                "type": "urn:noaa:nws:api:UnexpectedProblem",
                "title": "Unexpected Problem",
                "status": 500,
                "detail": "An unexpected problem has occurred.",
                "instance": "urn:noaa:nws:api:request:493c3a1d-f87e-407f-ae2c-24483f5aab63",
                "correlationId": "493c3a1d-f87e-407f-ae2c-24483f5aab63",
                "additionalProp1": {}
            }
            self.status_code = 500

        def json(self):
            return self.json_data

        def raise_for_status(self):
            raise requests.HTTPError

    return MockResponse()


def test_print_region_codes(capsys):
    apiclient.print_region_codes({"ABQ": "Albuquerque, NM", "ABR": "Aberdeen, SD"})
    captured = capsys.readouterr()
    assert "ABQ Albuquerque, NM\nABR Aberdeen, SD" in captured.out


def test_500_afd_response(monkeypatch, caplog):
    """Test API returning 500 when fetching list of AFD products"""
    requests_mock = Mock(side_effect=mocked_requests_get)
    monkeypatch.setattr('requests.get', requests_mock)
    response = apiclient.fetch_afd("ERR")
    assert response == {'response': None, 'error': "HTTP error fetching list of AFD products"}
    assert "HTTP error fetching list of AFD products" in caplog.text


def test_500_response(monkeypatch, caplog):
    """Test API returning 500 on any request"""
    requests_mock = Mock(side_effect=mocked_requests_get_500)
    monkeypatch.setattr('requests.get', requests_mock)
    response = apiclient.fetch_afd("PSR")
    assert response == {'response': None, 'error': "HTTP error fetching list of region codes"}
    assert "HTTP error fetching list of region codes" in caplog.text


def test_psr_response(monkeypatch):
    """Test fetching an example AFD for PSR region, without monitoring cache"""
    requests_mock = Mock(side_effect=mocked_requests_get)
    monkeypatch.setattr('requests.get', requests_mock)
    api_response = apiclient.fetch_afd("PSR")
    assert api_response['error'] is None
    assert api_response['response'] is not None
    assert api_response['response']['id'] == "1d6cd33d-4017-4dd1-8dce-41d4541de35a"
    assert api_response['response']['productCode'] == "AFD"
    assert api_response['response']['productName'] == "Area Forecast Discussion"
    assert "\n000\nFXUS65 KPSR 091229\nAFDPSR\n\nArea Forecast Discussion\nNational Weather " \
           "Service Phoenix AZ\n529 AM MST Thu Feb 9 2023\n\n" \
           in api_response['response']['productText']


def test_top_response(monkeypatch):
    """Test fetching an example AFD for TOP region, without monitoring cache"""
    requests_mock = Mock(side_effect=mocked_requests_get)
    monkeypatch.setattr('requests.get', requests_mock)
    api_response = apiclient.fetch_afd("TOP")
    assert api_response['error'] is None
    assert api_response['response'] is not None
    assert api_response['response']['id'] == "1f29f93c-583b-4144-ae22-8624a5e56504"
    assert api_response['response']['productCode'] == "AFD"
    assert api_response['response']['productName'] == "Area Forecast Discussion"
    assert "\n000\nFXUS63 KTOP 122335\nAFDTOP\n\nArea Forecast Discussion\nNational Weather " \
           "Service Topeka KS\n535 PM CST Sun Feb 12 2023" \
           in api_response['response']['productText']

def test_lox_response(monkeypatch):
    """Test fetching an example AFD for LOX region, without monitoring cache"""
    requests_mock = Mock(side_effect=mocked_requests_get)
    monkeypatch.setattr('requests.get', requests_mock)
    api_response = apiclient.fetch_afd("LOX")
    assert api_response['error'] is None
    assert api_response['response'] is not None
    assert api_response['response']['id'] == "a922a688-acb5-4bb8-8a22-55c6a107b61d"
    assert api_response['response']['productCode'] == "AFD"
    assert api_response['response']['productName'] == "Area Forecast Discussion"
    assert "\n000\nFXUS66 KLOX 130046\nAFDLOX\n\nArea Forecast Discussion...UPDATED\nNational " \
           "Weather Service Los Angeles/Oxnard CA \n446 PM PST Sun Feb 12 2023" \
           in api_response['response']['productText']

def test_okx_response(monkeypatch):
    """Test fetching an example AFD for OKX region, without monitoring cache"""
    requests_mock = Mock(side_effect=mocked_requests_get)
    monkeypatch.setattr('requests.get', requests_mock)
    api_response = apiclient.fetch_afd("OKX")
    assert api_response['error'] is None
    assert api_response['response'] is not None
    assert api_response['response']['id'] == "6893e2af-17ef-471a-b7bc-4a74a8af0374"
    assert api_response['response']['productCode'] == "AFD"
    assert api_response['response']['productName'] == "Area Forecast Discussion"
    assert "\n000\nFXUS61 KOKX 130251\nAFDOKX\n\nArea Forecast Discussion\nNational Weather " \
           "Service New York NY\n951 PM EST Sun Feb 12 2023" \
           in api_response['response']['productText']