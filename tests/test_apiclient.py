"""Test sendafd.apiclient module"""

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
    elif args[0] == "https://api.weather.gov/products/types/AFD/locations":
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
                "ERR": "Fake region for testing API error handling",
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

    return MockResponse(None, 404)


def test_print_region_codes(capsys):
    apiclient.print_region_codes({"ABQ": "Albuquerque, NM", "ABR": "Aberdeen, SD"})
    captured = capsys.readouterr()
    assert "ABQ Albuquerque, NM\nABR Aberdeen, SD" in captured.out


def test_500_response(monkeypatch, caplog):
    requests_mock = Mock(side_effect=mocked_requests_get)
    monkeypatch.setattr('requests.get', requests_mock)
    response = apiclient.fetch_afd("ERR")
    assert response == {'response': None, 'error': "HTTP error fetching list of AFD products"}
    print(caplog.text)
    assert "HTTP error fetching list of AFD products" in caplog.text
